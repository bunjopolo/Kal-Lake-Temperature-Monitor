        // Function to fetch data from the backend CHANGE THE VIEW LATER
        async function fetchData() {
            try {
                const response = await fetch('data/'); // Replace with your API endpoint
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Error fetching data:', error);
                return null;
            }
        }

        // Function to create the temperature graph
        async function tempGraph() {
            const data = await fetchData();

            if (data) {
                const dates = data.dates;
                const temperatures = data.temperatures;

                const ctx = document.getElementById('temperature-chart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: dates,
                        datasets: [{
                            label: 'Temperature (C°)',
                            data: temperatures,
                            borderColor: '#2980b9',
                            fill: false,
                        }]
                    },
                    options: {
                        // Customize chart options here
                    }
                });
            }
        }

        async function monthlyAvgGraph() {
            const data = await fetchData();

            if (data) {
                const avg = data.monthly_avg;
            

                const ctx = document.getElementById('monthly-avg-chart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                        'October', 'November', 'December'],
                        datasets: [{
                            label: 'Average Temperature (C°)',
                            data: avg,
                            backgroundColor: '#2980b9',
                            borderColor: '#2980b9',
                            fill: false,
                        }]
                    },
                    options: {
                        // Customize chart options here
                    }
                });
            }
            

        }

        // Call the function to create the graph when the page loads
        document.addEventListener('DOMContentLoaded', tempGraph);
        document.addEventListener('DOMContentLoaded', monthlyAvgGraph);