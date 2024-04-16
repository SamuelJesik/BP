console.log("Script loaded");

document.addEventListener('DOMContentLoaded', (event) => {
    console.log("DOM fully loaded and parsed");


    
    // Initialize the Ace Editor
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");
    console.log("Ace Editor initialized");


    var readOnlyEditor = ace.edit("readonly-editor");
    readOnlyEditor.setTheme("ace/theme/monokai");
    readOnlyEditor.session.setMode("ace/mode/python");
    readOnlyEditor.setValue(readOnlyCode, -1);
    readOnlyEditor.setReadOnly(true);  // Make it read-only

    //runcode

    



    // Initialize the Unit Tests Ace Editor
    var unitTestsEditor = ace.edit("unit-tests-editor");
    unitTestsEditor.setTheme("ace/theme/monokai");
    unitTestsEditor.session.setMode("ace/mode/python"); // or another appropriate mode for unit tests
    unitTestsEditor.setValue(expectedOutput, -1); // Nastavenie hodnoty editora na obsah expected_output
    unitTestsEditor.setReadOnly(true); // Set to true if it should be read-only




    // Get the DOM elements for the file input, custom button, and file name display
    var uploadBtnElement = document.getElementById('uploadBtn');
    var fileInputElement = document.getElementById('fileInput');
    var fileChosenElement = document.getElementById('file-chosen');
    


    // Získanie modálneho elementu
    var modal = document.getElementById("testResultsModal");
    // Získanie elementu <span>, ktorý zatvára modálne okno
    var span = document.getElementsByClassName("close-button")[0];
    // Získanie elementu pre výstup testov
    var testOutput = document.getElementById("test-results-output");
    // Globálna premenná pre uchovanie výsledkov testov
    var lastTestResults = "";

    var showResultsButton = document.getElementById('show-results');
    showResultsButton.addEventListener('click', function() {
    if (lastTestResults) {
        // Ak existujú uložené výsledky testov, zobrazíme ich v modálnom okne
        testOutput.innerHTML = lastTestResults;
        modal.style.display = "block";
    } else {
        console.log("Žiadne výsledky testov na zobrazenie.");
    }
});

    // Keď užívateľ klikne na <span> (x), zatvor modálne okno
    span.onclick = function() {
    modal.style.display = "none";
  }
  
    // Keď užívateľ klikne mimo modálneho okna, zatvor ho
    window.onclick = function(event) {
        if (event.target == modal) {
        modal.style.display = "none";
        }
    }

    // Check if the elements exist
    if (uploadBtnElement && fileInputElement) {
        console.log("Upload button and file input found");

        // Event listener for the custom 'Choose File' button
        uploadBtnElement.addEventListener('click', () => {
            console.log("Custom 'Choose File' button clicked");
            fileInputElement.click(); // Trigger the hidden file input click
        });

        // Event listener for the hidden file input change
        fileInputElement.addEventListener('change', (event) => {
            console.log("File input changed");
            var file = event.target.files[0];
            if (file) {
                console.log("File chosen:", file.name);

                // Display the file name
                fileChosenElement.textContent = file.name;

                // Update the Ace Editor with the contents of the file
                var reader = new FileReader();
                reader.onload = function(e) {
                    editor.setValue(e.target.result);
                    console.log("Ace Editor updated with file content");
                };
                reader.readAsText(file);
            } else {
                fileChosenElement.textContent = 'No file chosen';
                console.log("No file chosen");
            }
        });
    }

        //runcode

// Predpokladáme, že CSRF token je v šablóne ako meta tag
var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Predpokladáme, že task_id je uložený ako data atribút v HTML elemente
var taskDataElement = document.getElementById('task-data');
var task_id = taskDataElement ? taskDataElement.dataset.taskId : null;

var runButton = document.getElementById('run-code');
runButton.addEventListener('click', function() {
    var code = editor.getSession().getValue();  // Assuming you're using Ace editor to get the code
    var data = JSON.stringify({ code: code });
    
    console.log("Run button clicked");
    console.log("Sending the following data to the server: ", data);

    // Kontrola, či máme task_id predtým, ako spravíme request
    if (task_id) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', `/myapp/run-code/${task_id}/`, true); // Použiť template literal pre vloženie task_id
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('X-CSRFToken', csrfToken); // Posielame CSRF token

        xhr.onload = function() {
            if (xhr.status == 200) {
                // Spracovanie odpovede
                var response = JSON.parse(xhr.responseText);
                var formattedStdout = response.code_stdout.replace(/\\n/g, '<br>');
                var formattedStderr = response.code_stderr.replace(/\\n/g, '<br>');
                var formattedTestStdout = response.test_stdout.replace(/\\n/g, '<br>');
                var formattedTestStderr = response.test_stderr.replace(/\\n/g, '<br>');
                var output = `
            <p><strong>Kód output:</strong> ${formattedStdout}</p>
            <p><strong>Code Stderr:</strong> ${formattedStderr || "No stderr output"}</p>
            <p><strong>Code Return Code:</strong> ${response.code_returncode}</p>
            <p><strong>Test output:</strong> ${formattedTestStdout}</p>
            <p><strong>Test Stderr:</strong> ${formattedTestStderr || "No stderr output"}</p>
            <p><strong>Test Return Code:</strong> ${response.test_returncode}</p>
        `;
                console.log('Výstup:', response.stdout);
                console.log('Chyby:', response.stderr);

                testOutput.innerHTML = output;
                modal.style.display = "block";
                // Save the formatted results for later display
                lastTestResults = output;

                // Zobraz tieto informácie v tvojom HTML
            } else {
                // V prípade chyby, zobraz informáciu o chybe
                console.error('Došlo k chybe pri spracovaní vašej požiadavky.');
            }
        };




        xhr.send(data);
    } else {
        console.error('Task ID is not defined.');
    }
});
    

    // Event listener for form submission
    var form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        console.log("Form submitted");
        if (fileInputElement.files.length === 0) {
            // If no file is set to the hidden input, prevent the form from submitting
            console.log("No file set to the hidden input, submission prevented.");
            event.preventDefault();
            // Optionally, trigger the file input to prompt the user
            fileInputElement.click();
        } else {
            console.log("File is set, proceeding with the form submission.");
            // The file is set, let the form submit normally
        }
    });
});


