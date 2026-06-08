console.log("dashboard.js loaded");

let cpuChart;
let lambdaChart;
let dynamodbChart;

async function loadCPUData() {

    try {

        const response =
            await fetch('/api/ec2/cpu');

        const result =
            await response.json();

        console.log(result);

        const cpuLabels =
            result.data.map(
                item => item.instance_id
            );

        const cpuValues =
            result.data.map(
                item => item.cpu_utilization
            );

        const averageCPU =

            cpuValues.length > 0

            ? (
                cpuValues.reduce(
                    (a, b) => a + b,
                    0
                ) / cpuValues.length
            ).toFixed(2)

            : 0;

        document.getElementById(
            'cpu-value'
        ).innerText =
            `${averageCPU}%`;

        const cpuCtx =
            document.getElementById(
                'cpuChart'
            );

        if (!cpuCtx) {

            throw new Error(
                'cpuChart canvas not found'
            );

        }

        if (cpuChart) {

            cpuChart.destroy();

        }

        cpuChart = new Chart(cpuCtx, {

            type: 'bar',

            data: {

                labels: cpuLabels,

                datasets: [{

                    label: 'CPU Utilization (%)',

                    data: cpuValues

                }]
            },

            options: {

                responsive: true,

                scales: {

                    y: {

                        beginAtZero: true,

                        max: 100,

                        title: {

                            display: true,

                            text: 'CPU %'
                        }
                    }
                }
            }
        });

    }

    catch(error) {

        console.error(
            'CPU chart error:',
            error
        );

        document.getElementById(
            'cpu-value'
        ).innerText =
            'Error';

    }
}
async function loadLambdaData() {

    try {

        const response = await fetch('/api/lambda');

        const result = await response.json();

        console.log(result);

        const lambdaCount = result.data.length;

        document.getElementById('lambda-count').innerText =
            lambdaCount;

        const lambdaLabels =
            result.data.map(
                item => item.function_name
            );

        const lambdaValues =
            result.data.map(
                () => 1
            );

        const lambdaCtx =
            document.getElementById('lambdaChart');

        if (lambdaChart) {

            lambdaChart.destroy();

        }

        lambdaChart = new Chart(lambdaCtx, {

            type: 'bar',

            data: {

                labels: lambdaLabels,

                datasets: [{

                    label: 'Lambda Functions',

                    data: lambdaValues

                }]
            }
        });

    }

    catch(error) {

        console.error(error);

    }
}

async function loadDynamoDBData() {

    try {

        const response =
            await fetch('/api/dynamodb');

        const result =
            await response.json();

        console.log(result);

        const tableCount =
            result.data.length;

        document.getElementById(
            'dynamodb-count'
        ).innerText = tableCount;

        const dynamoLabels =
            result.data.map(
                item => item.table_name
            );

        const dynamoValues =
            result.data.map(
                item => item.item_count
            );

        const dynamoCtx =
            document.getElementById(
                'dynamodbChart'
            );

        if (dynamodbChart) {

            dynamodbChart.destroy();

        }

        dynamodbChart = new Chart(dynamoCtx, {

            type: 'bar',

            data: {

                labels: dynamoLabels,

                datasets: [{

                    label: 'DynamoDB Item Count',

                    data: dynamoValues

                }]
            },

            options: {

                responsive: true,

                scales: {

                    y: {

                        beginAtZero: true,

                        title: {

                            display: true,

                            text: 'Items'
                        }
                    }
                }
            }
        });

    }

    catch(error) {

        console.error(
            'DynamoDB chart error:',
            error
        );

    }
}

async function refreshDashboard() {

    console.log("Refreshing dashboard...");

    await loadCPUData();

    await loadLambdaData();

    await loadDynamoDBData();

}

loadCPUData();
loadLambdaData();
loadDynamoDBData();
refreshDashboard();
setInterval(refreshDashboard, 60000);
