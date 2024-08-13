document.getElementById('runCode').addEventListener('click', () => {
  const urlBox = document.getElementById('urlBox').value;

  fetch('http://localhost:5000/run_python_code', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: urlBox })
  })
  .then(response => response.json())
  .then(data => {
      console.log('Response from backend:', data);
      alert(data.message);
  })
  .catch(error => console.error('Error:', error));
});
