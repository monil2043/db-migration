const { DynamoDBClient,
    BatchWriteItemCommand,
} = require("@aws-sdk/client-dynamodb");
const { fromIni } = require("@aws-sdk/credential-providers");
const { loadSharedConfigFiles } = require("@aws-sdk/shared-ini-file-loader");

const fsPromises = require("fs").promises;
//--tableName "migrate-data" --sourceFile data.json --accessKeyId $AWS_ACCESS_KEY_ID --secretAccessKey $AWS_SECRET_ACCESS_KEY

const argv = require("yargs/yargs")(process.argv.slice(2))
    .usage("Usage: $0 --tableName [--sourceFile] [--profile]")
    .demandOption(["tableName"])
    .describe("tableName", "Specify table to import")
    .describe(
        "sourceFile",
        "optionally override the source items filename (vs $table_items)"
    )
    .describe("profile", "optionally specify AWS profile").argv;

let sourceItemsPath = `data.json`;
if (argv.sourceFile) {
    sourceItemsPath = argv.sourceFile;
}

(async () => {
    let config = {};
    if (argv.profile) {
        const sharedConfig = await loadSharedConfigFiles();
        console.log(sharedConfig)
        console.log(sharedConfig.configFile[argv.profile])
        const region = "us-west-2";
        config = {
            credentials: fromIni({ profile: argv.profile }),
            region,
        };
    }

    const client = new DynamoDBClient(config);
    try {
        const batchSize = 25;
        const items = JSON.parse(await fsPromises.readFile(sourceItemsPath));
        console.log(`read ${items.length} items`);
        const batches = [];
        for (let i = 0; i < items.length; i += batchSize) {
            batches.push(items.slice(i, i + batchSize));
        }
        console.log(`writing with ${batches.length} batches`);
        for (const batch of batches) {
            const putRequests = batch.map((item) => {
                return { PutRequest: { Item: item } };
            });
            const command = new BatchWriteItemCommand({
                RequestItems: {
                    [`${argv.tableName}`]: putRequests,
                },
            });
            // console.log(JSON.stringify(command.input));
            results = await client.send(command);
            console.log(results);
        }
    } catch (err) {
        console.error(err);
    }
})();
