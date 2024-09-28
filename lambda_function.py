# lambda_function.py
import json

def lambda_handler(event, context):
    # Process incoming traffic data
    traffic_data = json.loads(event['body'])
    
    # Example: Log traffic level
    traffic_level = traffic_data.get('traffic_level', 0)
    print(f"Traffic Level: {traffic_level}")
    
    # Here, you can integrate with other services like databases or Kafka
    
    return {
        'statusCode': 200,
        'body': json.dumps('Traffic data processed successfully!')
    }
