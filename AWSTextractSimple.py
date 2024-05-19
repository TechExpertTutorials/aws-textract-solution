"""
need to install boto3 package (AWS SDK) from conda -c conda-forge 
pip install boto3

conda create -n aws-cloud  
conda install -c conda-forge boto3 ipykernel jupyterlab notebook python=3.12.0  
** to set up env as new kernel in jupyterlabs:  
python -m ipykernel install --user --name=gcp-cloud

repo: https://github.com/donaldsrepo/aws-textract-solution

setup credentials:

~/.aws/credentials

[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

"""
import boto3

# if ~/.aws/credentials not configured
# client = boto3.client('textract', 
#                       region_name='<aws-region>', 
#                       aws_access_key_id='<Your access key here>',
#                       aws_secret_access_key='<Your secret access key here>')
# else
client = boto3.client('textract')

# image to read text from
with open('dl1.png', 'rb') as file:
    img_test = file.read()
    bytes_test = bytearray(img_test)

response = client.analyze_document(Document={'Bytes': bytes_test},FeatureTypes = ['TABLES'])
print(response)

blocks = response['Blocks']
text = ""
for block in blocks:
    if block['BlockType'] == 'WORD':
        text += block['Text'] + "\n"
print(text)

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

# print(get_kv_map(blocks))

lines, blocks, confidences = get_lines(blocks)

for line in lines:
    print(f"Text: {lines[line]} Confidence: {confidences[line]}")