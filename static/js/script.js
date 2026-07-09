const summarizeBtn = document.getElementById("summarizeBtn");

const loading = document.getElementById("loading");

const summaryBox = document.getElementById("summaryBox");

const downloadBtn = document.getElementById("downloadBtn");

summarizeBtn.addEventListener("click", async () => {

    const fileInput = document.getElementById("fileInput");

    if(fileInput.files.length===0){

        alert("Please select a document.");

        return;

    }

    const formData = new FormData();

    formData.append("file", fileInput.files[0]);

    loading.style.display="block";

    summaryBox.value="";

    try{

        const response = await fetch("/summarize",{

            method:"POST",

            body:formData

        });

        const data = await response.json();

        loading.style.display="none";

        if(response.ok){

            summaryBox.value=data.summary;

        }

        else{

            summaryBox.value=data.detail;

        }

    }

    catch(error){

        loading.style.display="none";

        summaryBox.value="Something went wrong.";

    }

});

downloadBtn.addEventListener("click",()=>{

    const summary = summaryBox.value;

    if(summary===""){

        alert("No summary available.");

        return;

    }

    const blob = new Blob([summary],{

        type:"text/plain"

    });

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href=url;

    a.download="summary.txt";

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);

    window.URL.revokeObjectURL(url);

});