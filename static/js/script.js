const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');
const summarizeBtn = document.getElementById('summarizeBtn');
const loading = document.getElementById('loading');
const summaryBox = document.getElementById('summaryBox');
const downloadBtn = document.getElementById('downloadBtn');
const copyBtn = document.getElementById('copyBtn');
const wordCount = document.getElementById('wordCount');
const emptyState = document.getElementById('emptyState');
const dropZone = document.getElementById('dropZone');
const uploadCard = document.querySelector('.upload-card');
const toast = document.getElementById('toast');
const toastMessage = document.querySelector('.toast-message');

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showToast(message, type = 'success') {
    toastMessage.textContent = message;
    toast.className = 'toast visible toast-' + type;
    setTimeout(() => {
        toast.classList.remove('visible');
    }, 3000);
}

function updateWordCount(text) {
    if (!text || text.trim() === '') {
        wordCount.textContent = '0 words';
        return;
    }
    const words = text.trim().split(/\s+/).filter(word => word.length > 0);
    wordCount.textContent = `${words.length} word${words.length !== 1 ? 's' : ''}`;
    emptyState.classList.add('hidden');
}

function toggleButtons(hasContent) {
    downloadBtn.disabled = !hasContent;
    copyBtn.disabled = !hasContent;
}

function handleFileSelect(file) {
    if (file) {
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
        const validExtensions = ['.pdf', '.docx', '.txt'];
        const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));

        if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
            showToast('Please upload a PDF, DOCX, or TXT file.', 'error');
            return;
        }

        fileInfo.classList.remove('hidden');
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        summarizeBtn.disabled = false;
    }
}

fileInput.addEventListener('change', (e) => {
    handleFileSelect(e.target.files[0]);
});

removeFile.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.value = '';
    fileInfo.classList.add('hidden');
    summarizeBtn.disabled = true;
});

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
    }, false);
});

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        uploadCard.classList.add('drag-over');
        dropZone.classList.add('drag-over');
    }, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        uploadCard.classList.remove('drag-over');
        dropZone.classList.remove('drag-over');
    }, false);
});

dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const file = dt.files[0];
    handleFileSelect(file);
}, false);

summarizeBtn.addEventListener('click', async () => {
    if (!fileInput || fileInput.files.length === 0) {
        showToast('Please select a document.', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    loading.classList.add('visible');
    summarizeBtn.disabled = true;
    summaryBox.value = '';

    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        loading.classList.remove('visible');
        summarizeBtn.disabled = false;

        if (response.ok) {
            summaryBox.value = data.summary;
            updateWordCount(data.summary);
            toggleButtons(true);
            showToast('Summary generated successfully!', 'success');
        } else {
            summaryBox.value = data.detail || 'An error occurred while processing your document.';
            updateWordCount('');
            toggleButtons(false);
            showToast('Failed to generate summary.', 'error');
        }
    } catch (error) {
        loading.classList.remove('visible');
        summarizeBtn.disabled = false;
        summaryBox.value = 'Something went wrong. Please try again.';
        updateWordCount('');
        toggleButtons(false);
        showToast('An error occurred. Please try again.', 'error');
    }
});

downloadBtn.addEventListener('click', () => {
    const summary = summaryBox.value;
    if (!summary || summary.trim() === '') {
        showToast('No summary available to download.', 'error');
        return;
    }

    const blob = new Blob([summary], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'summary.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    showToast('Summary downloaded successfully!', 'success');
});

copyBtn.addEventListener('click', async () => {
    const summary = summaryBox.value;
    if (!summary || summary.trim() === '') {
        showToast('No summary available to copy.', 'error');
        return;
    }

    try {
        await navigator.clipboard.writeText(summary);
        showToast('Summary copied to clipboard!', 'success');
    } catch (err) {
        const textArea = document.createElement('textarea');
        textArea.value = summary;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('Summary copied to clipboard!', 'success');
        } catch (e) {
            showToast('Failed to copy summary.', 'error');
        }
        document.body.removeChild(textArea);
    }
});

summaryBox.addEventListener('input', () => {
    if (summaryBox.value) {
        updateWordCount(summaryBox.value);
        toggleButtons(!!summaryBox.value.trim());
    }
});

document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!summarizeBtn.disabled) {
            summarizeBtn.click();
        }
    }
});
