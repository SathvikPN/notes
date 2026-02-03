"""
Run both REST and GraphQL examples side-by-side for comparison
"""

import subprocess
import sys
import time

def run_rest_examples():
    """Run REST API examples"""
    print("\n" + "🔴" * 35)
    print("  RUNNING REST API EXAMPLES")
    print("🔴" * 35)
    subprocess.run([sys.executable, "src/client/rest_examples.py"])
    time.sleep(2)

def run_graphql_examples():
    """Run GraphQL API examples"""
    print("\n" + "🟢" * 35)
    print("  RUNNING GRAPHQL API EXAMPLES")
    print("🟢" * 35)
    subprocess.run([sys.executable, "src/client/graphql_examples.py"])

def main():
    """Run both example sets"""
    print("\n" + "=" * 70)
    print("  REST vs GraphQL - Side-by-Side Comparison")
    print("=" * 70)
    print("\nℹ️  Make sure both servers are running:")
    print("   Terminal 1: python src/rest/server.py")
    print("   Terminal 2: python src/graphql/server.py")
    print("\n" + "=" * 70)
    
    input("\nPress Enter to start REST examples...")
    run_rest_examples()
    
    input("\nPress Enter to start GraphQL examples...")
    run_graphql_examples()
    
    print("\n" + "=" * 70)
    print("  🎯 COMPARISON COMPLETE")
    print("=" * 70)
    print("\n📊 Key Takeaways:")
    print("\n🔴 REST API:")
    print("   • Multiple endpoints")
    print("   • Over-fetching (all fields returned)")
    print("   • Under-fetching (multiple requests for nested data)")
    print("   • N+1 problem")
    print("\n🟢 GraphQL API:")
    print("   • Single endpoint")
    print("   • Precise field selection")
    print("   • Nested data in one request")
    print("   • No N+1 problem")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
