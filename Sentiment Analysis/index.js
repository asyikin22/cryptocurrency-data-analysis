// console.log('hello bitches')

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