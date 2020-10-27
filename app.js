d3
    .csv("../csvs/states.csv")
    .then(makeChart);

function makeChart(data) {
    var State = data.map(function (d) {
        return d.State;
    });
    var Cases = data.map(function (d) {
        return d.Cases;
    });
// Bar chart
    new Chart(document.getElementById("myCanvas"), {
        type: 'bar',
        data: {
            labels: State,
            datasets: [
                {
                    label: "Population (millions)",
                    backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
                    data: value
                }
            ]
        },
        options: {
            legend: {display: false},
            title: {
                display: true,
                text: 'Total Confirmed Cases of COVID in May'
            }
        }
    });
}
