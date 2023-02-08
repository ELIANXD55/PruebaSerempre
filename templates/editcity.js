document.querySelector('#form').addEventListener('submit', function(event) {
    event.preventDefault();

    const id = document.querySelector('#id').value;
    const code = document.querySelector('#code').value;
    const city = document.querySelector('#city').value;
    console.log(id, code, city);

  });