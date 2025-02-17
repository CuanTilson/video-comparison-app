document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('upload-form');
    const videoBeforeInput = document.getElementById('video_before');
    const videoAfterInput = document.getElementById('video_after');
    const resultsContainer = document.getElementById('results');
    const changesContainer = document.getElementById('changes');
    const downloadLink = document.getElementById('download-report');

    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();
        console.log('Form submitted'); // Debugging statement
        const videoBefore = videoBeforeInput.files[0];
        const videoAfter = videoAfterInput.files[0];

        if (videoBefore && videoAfter) {
            const formData = new FormData();
            formData.append('video_before', videoBefore);
            formData.append('video_after', videoAfter);

            console.log('Sending request to /upload'); // Debugging statement
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
                .then(response => {
                    console.log('Response received:', response); // Debugging statement
                    return response.json();
                })
                .then(data => {
                    console.log('Data received:', data); // Debugging statement
                    if (data.report_url) {
                        downloadLink.href = data.report_url;
                        downloadLink.style.display = 'block';
                        console.log('Download link updated:', downloadLink.href); // Debugging statement
                    } else {
                        console.error('No report URL in response'); // Debugging statement
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            alert('Please upload both videos.');
        }
    });

    function displayResults(data) {
        changesContainer.innerHTML = '';
        if (data.differences.length > 0) {
            data.differences.forEach(diff => {
                const img = document.createElement('img');
                img.src = diff.highlighted_frame;
                img.alt = 'Detected Difference';
                changesContainer.appendChild(img);
            });
            resultsContainer.classList.add('active');
        } else {
            changesContainer.innerHTML = '<p>No differences detected.</p>';
            resultsContainer.classList.add('active');
        }
    }
});