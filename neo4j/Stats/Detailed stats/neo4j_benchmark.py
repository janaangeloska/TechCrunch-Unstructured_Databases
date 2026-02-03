from neo4j import GraphDatabase
import time
import statistics
import getpass

URI = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"

QUERY = """ (query goes here) """


def run_query_with_profile(driver, query, run_number):
    """Executes query with PROFILE and returns time taken"""
    with driver.session() as session:
        # Client-side timing (end-to-end)
        start_time = time.time()

        # Execute query with PROFILE
        result = session.run(f"PROFILE {query}")

        # List of all the results
        records = list(result)

        # Summary
        summary = result.consume()

        end_time = time.time()
        client_time_ms = (end_time - start_time) * 1000

        # Exact server-side timings from summary
        server_exec_time = summary.result_available_after  # Query execution time
        server_fetch_time = summary.result_consumed_after  # Total time including fetching results

        # dbHits - (number of low-level storage accesses Neo4j makes to read
        # nodes, relationships, properties, or indexes while executing a query).
        profile = summary.profile
        total_db_hits = 0

        def count_db_hits(p):
            """Recursively sums dbHits"""
            if not p:
                return 0
            hits = p.get('dbHits', 0)
            for child in p.get('children', []):
                hits += count_db_hits(child)
            return hits

        if profile:
            total_db_hits = count_db_hits(profile)

        print(f"Run {run_number:2d}: Client: {client_time_ms:7.2f} ms | "
              f"Server Exec: {server_exec_time:6.2f} ms | "
              f"Server Total: {server_fetch_time:7.2f} ms | "
              f"dbHits: {total_db_hits:7d} | Results: {len(records)}")

        return client_time_ms, server_exec_time, server_fetch_time, total_db_hits, len(records)


def main():
    print("Neo4j - 30 runs")

    print(f"Neo4j URI: {URI}")
    print(f"Username: {USERNAME}")
    print("Connecting to Neo4j...")

    driver = None
    try:
        driver = GraphDatabase.driver(URI, auth=(USERNAME, ""))
        with driver.session() as session:
            session.run("RETURN 1")
        print("Success! (without password)")
    except Exception:
        print("Cannot connect without password")
        if driver:
            driver.close()

        PASSWORD = getpass.getpass("Enter password (or press Enter): ")
        try:
            driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
            with driver.session() as session:
                session.run("RETURN 1")
            print("Successfully connected")
        except Exception as e:
            print(f"Error: {e}")
            return

    print(f"\nQuery:\n{QUERY}")

    try:
        client_times = []
        server_exec_times = []
        server_total_times = []
        db_hits_list = []

        print("Query execution (30 runs)")
        print("Client = full time | Server Exec = query execution | Server Total = including fetch")
        print()

        for i in range(1, 31):
            client_t, server_exec_t, server_total_t, db_hits, num_results = run_query_with_profile(driver, QUERY, i)
            client_times.append(client_t)
            server_exec_times.append(server_exec_t)
            server_total_times.append(server_total_t)
            db_hits_list.append(db_hits)

        print("Results")

        print("CLIENT-SIDE TIME (end-to-end including Python overhead):\n")
        print(f"Minimum:                {min(client_times):8.2f} ms")
        print(f"Maximum:                {max(client_times):8.2f} ms")
        print(f"Average:                {statistics.mean(client_times):8.2f} ms")
        print(f"Median:                 {statistics.median(client_times):8.2f} ms")
        print(f"Standard deviation:     {statistics.stdev(client_times):8.2f} ms")

        print(f"SERVER EXECUTION TIME (only query execution on server):\n")
        print(f"Minimum:                {min(server_exec_times):8.2f} ms")
        print(f"Maximum:                {max(server_exec_times):8.2f} ms")
        print(f"Average:                {statistics.mean(server_exec_times):8.2f} ms  ← Same as in Browser!")
        print(f"Median:                 {statistics.median(server_exec_times):8.2f} ms")
        print(f"Standard deviation:     {statistics.stdev(server_exec_times):8.2f} ms")

        print(f"SERVER TOTAL TIME (query + fetching results):\n")
        print(f"Minimum:                {min(server_total_times):8.2f} ms")
        print(f"Maximum:                {max(server_total_times):8.2f} ms")
        print(f"Average:                {statistics.mean(server_total_times):8.2f} ms")
        print(f"Median:                 {statistics.median(server_total_times):8.2f} ms")
        print(f"Standard deviation:     {statistics.stdev(server_total_times):8.2f} ms")

        avg_exec = statistics.mean(server_exec_times)
        avg_total = statistics.mean(server_total_times)
        avg_client = statistics.mean(client_times)

        fetch_overhead = avg_total - avg_exec
        python_overhead = avg_client - avg_total

        print(f"Summary:")
        print(f"Query execution (server):        {avg_exec:7.2f} ms")
        print(f"+ Fetch results (server)::        {fetch_overhead:7.2f} ms")
        print(f"+ Python/network overhead:         {python_overhead:7.2f} ms")
        print(f"= Total (client):                 {avg_client:7.2f} ms")

        with open('benchmark_results.txt', 'w', encoding='utf-8') as f:
            f.write("Neo4j Query Benchmark Results\n")
            f.write(f"Query:\n{QUERY}\n")

            f.write("CLIENT-SIDE TIME:\n")
            f.write(f"Minimum:      {min(client_times):8.2f} ms\n")
            f.write(f"Maximum:      {max(client_times):8.2f} ms\n")
            f.write(f"Average:      {statistics.mean(client_times):8.2f} ms\n")
            f.write(f"Median:       {statistics.median(client_times):8.2f} ms\n")
            f.write(f"Std Dev:      {statistics.stdev(client_times):8.2f} ms\n\n")

            f.write("SERVER EXECUTION TIME (same as Browser):\n")
            f.write(f"Minimum:      {min(server_exec_times):8.2f} ms\n")
            f.write(f"Maximum:      {max(server_exec_times):8.2f} ms\n")
            f.write(f"Average:      {statistics.mean(server_exec_times):8.2f} ms\n")
            f.write(f"Median:       {statistics.median(server_exec_times):8.2f} ms\n")
            f.write(f"Std Dev:      {statistics.stdev(server_exec_times):8.2f} ms\n\n")

            f.write("Detailed results:\n\n")
            for i, (ct, set, stt, dh) in enumerate(
                    zip(client_times, server_exec_times, server_total_times, db_hits_list), 1):
                f.write(f"Run {i:2d}: Client: {ct:7.2f} ms | Server Exec: {set:6.2f} ms | "
                        f"Server Total: {stt:7.2f} ms | dbHits: {dh:7d}\n")

    finally:
        if driver:
            driver.close()


if __name__ == "__main__":
    main()
