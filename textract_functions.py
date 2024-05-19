import boto3

# If you are processing a form document, this will extract Key-Value Pairs from your document
def get_kv_map(blocks):
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET" and 'KEY' in block['EntityTypes']:
            key_map[block_id] = block
        # else:
        #     value_map[block_id] = block
    return key_map, value_map, block_map

# Extracting LINES from an Image
def get_lines(blocks):
    line_map = {}
    block_map = {}
    confidence_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "LINE":
            line_map[block_id] = block['Text']
            confidence_map[block_id] = block['Confidence']
        else:
            block_map[block_id] = block
    return line_map, block_map, confidence_map