console.log("dashboard.js loaded");

let cpuChart;
let lambdaChart;
let dynamodbChart;

async function loadStatusData() {

    try {

        const response =
            await fetch('/api/status');

        const result =
            await response.json();

        let html = '';

        result.data.forEach(instance => {

            html += `
                <p>
                    <strong>${instance.instance_name}</strong><br>
                    State: ${instance.state}<br>
                    AZ: ${instance.availability_zone}
                </p>
                <hr>
            `;

        });

        document.getElementById(
            'system-status'
        ).innerHTML = html;

    }

    catch(error) {

        console.error(error);

        document.getElementById(
            'system-status'
        ).innerHTML =
            'Unable to load status';

    }
}

async function loadAlarmData() {

    try {

        const response =
            await fetch('/api/alarms');

        const result =
            await response.json();

        let html = '';

        if (result.data.length === 0) {

            html =
                '<p>No Active Alarms</p>';

        }

        else {

            result.data.forEach(alarm => {

                html += `
                    <p>
                        ${alarm.name}<br>
                        ${alarm.state}
                    </p>
                `;

            });

        }

        document.getElementById(
            'active-alarms'
        ).innerHTML = html;

    }

    catch(error) {

        console.error(error);

        document.getElementById(
            'active-alarms'
        ).innerHTML =
            'Unable to load alarms';

    }
}

async function loadSystemHealth() {

    try {

        const response =
            await fetch('/api/system-health');

        const result =
            await response.json();

        let html = '';

        result.data.forEach(instance => {

            html += `
                <p>
                    ${instance.instance_id}<br>
                    Health:
                    ${instance.cpu_health}
                </p>
                <hr>
            `;

        });

        document.getElementById(
            'system-health'
        ).innerHTML = html;

    }

    catch(error) {

        console.error(error);

        document.getElementById(
            'system-health'
        ).innerHTML =
            'Unable to load health';

    }
}

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

async function loadAlarms() {

    try {

        const response =
            await fetch('/api/alarms');

        const result =
            await response.json();

        console.log(
            "Alarm Data:",
            result
        );

        let html = '';

        if (
            result.data.length === 0
        ) {

            html =
                '<p>No active alarms</p>';

        }

        else {

            result.data.forEach(
                alarm => {

                    html += `
                    <div>
                        <strong>
                            ${alarm.alarm_name}
                        </strong><br>

                        State:
                        ${alarm.state}<br>

                        Metric:
                        ${alarm.metric}<br>

                        Updated:
                        ${alarm.updated}
                    </div>
                    <hr>
                    `;
                }
            );
        }

        document.getElementById(
            'alarms-container'
        ).innerHTML = html;

    }

    catch(error) {

        console.error(
            'Alarm widget error:',
            error
        );

        document.getElementById(
            'alarms-container'
        ).innerHTML =
            '<p>Error loading alarms</p>';
    }
}

async function loadSystemHealth() {

    try {

        const response =
            await fetch(
                '/api/system-health'
            );

        const result =
            await response.json();

        console.log(
            "Health Data:",
            result
        );

        let html = '';

        result.data.forEach(
            item => {

                html += `
                <div>
                    <strong>
                        ${item.instance_id}
                    </strong><br>

                    CPU:
                    ${item.cpu_utilization}%<br>

                    Health:
                    ${item.cpu_health}
                </div>
                <hr>
                `;
            }
        );

        document.getElementById(
            'health-container'
        ).innerHTML = html;

    }

    catch(error) {

        console.error(
            'Health widget error:',
            error
        );

        document.getElementById(
            'health-container'
        ).innerHTML =
            '<p>Error loading health data</p>';
    }
}

async function loadRemediationHistory() {

    try {

        const response =
            await fetch(
                '/api/remediation-history'
            );

        const result =
            await response.json();

        console.log(
            "Remediation History:",
            result
        );

        let html = '';

        if (
            result.data.length === 0
        ) {

            html =
                '<p>No remediation events found</p>';

        }

        else {

            result.data.forEach(
                event => {

                    html += `
                    <div>
                        <strong>
                            ${event.timestamp}
                        </strong><br>

                        Action:
                        ${event.action}<br>

                        Status:
                        ${event.status}<br>

                        Instance:
                        ${event.instance_id}
                    </div>
                    <hr>
                    `;
                }
            );
        }

        document.getElementById(
            'remediation-container'
        ).innerHTML = html;

    }

    catch(error) {

        console.error(
            'Remediation widget error:',
            error
        );

        document.getElementById(
            'remediation-container'
        ).innerHTML =
            '<p>Error loading remediation history</p>';
    }
}



async function refreshDashboard() {

    console.log(
        "Refreshing dashboard..."
    );

    await loadCPUData();

    await loadLambdaData();

    await loadDynamoDBData();

    await loadAlarms();

    await loadSystemHealth();

    await loadRemediationHistory();
}


refreshDashboard();

setInterval(
    refreshDashboard,
    60000
);



