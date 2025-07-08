import argparse
from tabulate import tabulate
from processor import process_csv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='CSV file')
    parser.add_argument('--where', help='Filter by: "price>100"')
    parser.add_argument('--aggregate', help='Example: "price=avg" or "rating=min"')
    parser.add_argument('--order-by', help='--order-by "rating=asc"')
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        result = process_csv(
            file_path=args.file,
            where=args.where,
            aggregate=args.aggregate,
            order=args.order_by)
        
        if args.aggregate and isinstance(result, dict):
            print(tabulate([result.values()], headers=result.keys(), tablefmt='grid'))
        elif isinstance(result, list):
            print(tabulate(result, headers='keys', tablefmt='grid'))
        else:
            print("No results found")
    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == '__main__':
    main()