## Questions

#### Why should one use Azure Key Vault when working in the Azure environment? What are the alternatives to using Azure Key Vault? What are the pros and cons of using Azure Key Vault?
We use Azure Key Vault to enhance data protection and compliance, to boost performance, and to achieve global scale. We could instead just use the keys, secrets and passwords directly, but they would not be encrypted so this would not be as safe. AKV has more data protection for compliance and scale, however it does take time to set up and may present a learning curve to new users. 

#### How do you achieve the loop functionality within an Azure Data Factory pipeline? Why would you need to use this functionality in a data pipeline?
The ForEach Activity defines a repeating control flow in an Azure Data Factory or Synapse pipeline. This activity is used to iterate over a collection and executes specified activities in a loop. More information can be found [here](https://docs.microsoft.com/en-us/azure/data-factory/control-flow-for-each-activity). We may need to use this functionality if a function needs to be repeated. For example, if we are processing data by month, we may want to loop the function over each month.

#### What are expressions in Azure Data Factory? How are they helpful when designing a data pipeline (please explain with an example)?
JSON values in the definition can be literal or expressions that are evaluated at runtime. For example: name can be defined as `"name":"value"` or `"name": "@pipeline().parameters.password"`. More information can be found [here](https://docs.microsoft.com/en-us/azure/data-factory/control-flow-expression-language-functions).

#### What are the pros and cons of parametrizing a dataset in Azure Data Factory pipeline’s activity?
Parameterizing a dataset increases flexibility and allows for automation. There is a slight learning curve, but given the right situation, it's a useful tool.

#### What are the different supported file formats and compression codecs in Azure Data Factory? When will you use a Parquet file over an ORC file? Why would you choose an AVRO file format over a Parquet file format? 
Azure supports the following file formats: 
- Avro format
- Binary format
- Delimited text format
- Excel format
- JSON format
- ORC format
- Parquet format
- XML format

Both ORC and Parquet are Hybrid file formats that combine both row based groups and column partitions. ORC is optimized for Hive whereas Parquet is optimized for Spark. Avro is row based, so it's better for systems with lots of writes. This makes it an ideal candidate for OLTP systems.
