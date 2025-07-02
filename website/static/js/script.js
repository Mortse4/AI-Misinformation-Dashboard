let navbar = document.querySelector('.navbar')

document.querySelector('#menu-bar').onclick = () =>{
    navbar.classList.toggle('active');
}


document.querySelector('#close').onclick = () =>{
    navbar.classList.remove('active');
}


window.onscroll = () =>{

    navbar.classList.remove('active');
    sortBar.classList.remove('active');

    if(window.scrollY > 100){
        document.querySelector('header').classList.add('active');
    }else{
        document.querySelector('header').classList.remove('active');
    }

}






function toggleMenu() {
    var list = document.querySelector('.list');
    list.style.display = list.style.display === 'none' ? 'flex' : 'none';
}





document.addEventListener("DOMContentLoaded", function() {
    var reportForm = document.getElementById("reportForm");
    reportForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission behavior
        validateForm();
    });
});

function validateForm() {
    var misinfoLink = document.getElementById("misinfo-link").value;
    var sourceLink = document.getElementById("source-link").value;
    var details = document.getElementById("Details").value;

    if (misinfoLink === "" || sourceLink === "" || details === "") {
        alert("Please fill in all fields.");
    } else {
        // Redirect to the success page
        window.location.href = "/report_misinformation.html";
    }
}






    // words
    const text = "ARTIFICIAL INTELLIGENCE MISINFORAMTION REPRESENTATION COMPUTATION EMPLOYMENT STUDY ALGORITHM PRACTICAL PROCESS APPLIED THEORETICAL DIGITAL COMMUNICATION ACCESS APPLICATION STORAGE PROMBLEM SOLVING INFORMATION AQUISITION AUTOMATED";
    
    function generateWordCloud(text) {
        const words = text.split(/\s+/); // Split text into words
        const wordCloudWords = [];
    
        words.forEach(word => {
            // Create an object for each word with text and weight
            const wordObject = {
                text: word,
                weight: Math.floor(Math.random() * 10) + 1 // Assign a random weight between 1 and 10
            };
            wordCloudWords.push(wordObject);
        });
    
        // Render the word cloud using jQCloud
        $("#wordCloud").jQCloud(wordCloudWords, {
            autoResize: true,
            fontSize: {
                from: 14, // Minimum font size
                to: 20 // Maximum font size
            },
            rotateRatio: 0.5, // Ratio of words that will be displayed vertically
            shape: 'star' // Specify the shape of the word cloud
        });
        }
    
        // Generate a random color
        function getRandomColor() {
        return '#' + Math.floor(Math.random()*16777215).toString(16); // Generate a random hexadecimal color
        }
    
        // Call the function with sample text
        generateWordCloud(text);
    

