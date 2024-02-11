function updateTextInput(val) {
    document.getElementById('step').value=val; 
    document.getElementById('slider').value=val;  
  }

  


function collecterDonneesEtEnvoyer() {
    const progression= document.querySelector('input[name="prog"]:checked')?.value;
    const  difficulty = document.querySelector('input[name="dif"]:checked')?.value;
    const percent = document.getElementById('slider').value;

    const data = {
      progression: progression,
      difficulty: difficulty,
      percent: percent
    };

    fetch('http://127.0.0.1:5000/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Succès:', data);
    })
    .catch((error) => {
        console.error('Erreur:', error);
    });
}

// Exécuter la fonction toutes les minutes
setInterval(collecterDonneesEtEnvoyer, 60000);
