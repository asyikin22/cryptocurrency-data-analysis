// console.log('hello bitches')

//show/hide the button based on scroll position
window.onscroll = function() {
    const backToTopButton = document.querySelector('.back-to-top');
    if(document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none"
    }
}

//function to scroll to top
function scrollToTop() {
    window.scrollTo({ top:0, behavior: 'smooth'})
}
 
//toggle function for currency converter widget
function toggleWidget() {
    const widget = document.querySelector('.converter-widget');
    widget.classList.toggle('active');
}

//toggle funciton for floating chart
function toggleFloat(chartId) {
    const selectedChart = document.getElementById(chartId);

    if (selectedChart) {
        selectedChart.classList.toggle("floating");
        makeDraggable(selectedChart);
    } else {
        console.error(`Element with ID ${chartId} not found`)
    }
}

//funcition to make charts draggable
function makeDraggable(chart) {
    let offsetX, offsetY;

    chart.onmousedown = function (e) {
        e.preventDefault();
        chart.classList.add('dragging');

        offsetX = e.clientX - chart.getBoundingClientRect().left;
        offsetY = e.clientY - chart.getBoundingClientRect().top;

        document.onmousemove = function (e) {
            const newX = e.clientX - offsetX
            const newY = e.clientY - offsetY

            const maxX = window.innerWidth - chart.offsetWidth;
            const maxY = window.innerHeight - chart.offsetHeight;

            chart.style.left = Math.max(0, Math.min(newX, maxX)) + 'px';
            chart.style.top = Math.max(0, Math.min(newY, maxY)) + 'px';
        }

        document.onmouseup = function () {
            chart.classList.remove('dragging')
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
};

//function to get price history from coin gecko
document.getElementById('price-search-form').addEventListener('submit', function(event){
    event.preventDefault();

    const date = document.getElementById('date').value;
    const coin = document.getElementById('coin').value;
    
    // Convert the date to dd-mm-yyyy format
    const[year, month, day] = date.split('-');
    const formattedDate = `${day}-${month}-${year}`;

    // Use the date directly in the fetch URL
    fetch(`https://api.coingecko.com/api/v3/coins/${coin}/history?date=${formattedDate}&localization=false`)
    .then(response => {
        if(!response.ok) {
            throw new Error('Data not found');
        }
        return response.json();
    })
    .then(data => {
        if (data.market_data && data.market_data.current_price) {
            const price = data.market_data.current_price.usd;
            document.getElementById('result').innerHTML =  `
                <h3>$${price}</h3>
            `;
        } else {
            document.getElementById('result').innerHTML =  `
                <h3>No price data available for this date</h3>
            `;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `
            <h3>${error.message}</h3>
        `;
    });
});
