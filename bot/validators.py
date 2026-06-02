import argparse

def validate_inputs(args):
    if args.type.upper() in ['LIMIT', 'STOP_LIMIT'] and not args.price:
        raise argparse.ArgumentError(None, "Price is required for LIMIT and STOP_LIMIT orders.")
    
    if args.type.upper() == 'STOP_LIMIT' and not args.stop_price:
        raise argparse.ArgumentError(None, "Stop price (--stop_price) is required for STOP_LIMIT orders.")
        
    if args.quantity <= 0:
        raise argparse.ArgumentError(None, "Quantity must be greater than zero.")
        
    if args.price is not None and args.price <= 0:
        raise argparse.ArgumentError(None, "Price must be greater than zero.")
        
    if args.stop_price is not None and args.stop_price <= 0:
        raise argparse.ArgumentError(None, "Stop price must be greater than zero.")
        
    return True