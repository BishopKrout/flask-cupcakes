// get cupcakes from API and add to list
axios.get('/api/cupcakes')
  .then(response => {
    const cupcakes = response.data.cupcakes;
    const cupcakeList = $('#cupcake-list');

    cupcakes.forEach(cupcake => {
      const listItem = $('<li>').text(`Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}, Image: ${cupcake.image}`);
      cupcakeList.append(listItem);
    });
  })
  .catch(error => console.error(error));

// handle form submission
$('#new-cupcake-form').on('submit', event => {
  event.preventDefault();

  const flavor = $('#flavor').val();
  const size = $('#size').val();
  const rating = $('#rating').val();
  const image = $('#image').val();

  const data = {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image
  };

  axios.post('/api/cupcakes', data)
    .then(response => {
      const cupcake = response.data.cupcake;
      const listItem = $('<li>').text(`Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}, Image: ${cupcake.image}`);
      $('#cupcake-list').append(listItem);
      $('#new-cupcake-form')[0].reset();
    })
    .catch(error => console.error(error));
});

axios.patch('/api/cupcakes/' + id, {
  flavor: flavor,
  size: size,
  rating: rating,
  image: image
}, {
  headers: {
    'Content-Type': 'application/json'
  }
})


