document.addEventListener('DOMContentLoaded', function() {
    const urlForm = document.getElementById('url-form');
    const urlInput = document.getElementById('url-input');
    const loader = document.getElementById('loader');
    const resultCard = document.getElementById('result-card');
    const resultHeader = document.getElementById('result-header');
    const resultIcon = document.getElementById('result-icon');
    const resultTitle = document.getElementById('result-title');
    const analyzedUrl = document.getElementById('analyzed-url');
    const verdict = document.getElementById('verdict');
    const confidence = document.getElementById('confidence');
    const featureList = document.getElementById('feature-list');
    const exampleButtons = document.querySelectorAll('.example-btn');
    
    // Example URL buttons
    exampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            urlInput.value = this.dataset.url;
            analyzeUrl(this.dataset.url);
        });
    });
    
    // Form submission
    urlForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        
        if (url) {
            analyzeUrl(url);
        }
    });
    
    // Function to analyze URL
    function analyzeUrl(url) {
        // Show loader
        loader.style.display = 'flex';
        resultCard.style.display = 'none';
        
        // Analyze URL
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loader
            loader.style.display = 'none';
            
            // Display results
            displayResults(url, data);
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Hide loader
            loader.style.display = 'none';
            
            // Display error
            displayError(url, error);
        });
    }
    
    // Function to display results
    function displayResults(url, data) {
        // Update analyzed URL
        analyzedUrl.textContent = url;
        
        // Update result header and verdict based on phishing status
        resultCard.className = 'result-card';
        
        if (data.is_phishing) {
            resultCard.classList.add('danger');
            resultIcon.className = 'fas fa-exclamation-triangle';
            resultTitle.textContent = 'Potential Phishing Detected';
            verdict.textContent = 'Potentially Dangerous';
        } else {
            resultCard.classList.add('safe');
            resultIcon.className = 'fas fa-check-circle';
            resultTitle.textContent = 'URL Analysis Result';
            verdict.textContent = 'Likely Safe';
        }
        
        // Set confidence
        confidence.textContent = `Confidence: ${Math.round(data.confidence)}% (${data.method || 'rule-based'})`;
        
        // Clear feature list
        featureList.innerHTML = '';
        
        // Add features to list
        const features = data.features;
        
        // Feature descriptions for better readability
        const featureDescriptions = {
            'suspicious_tld': 'Suspicious top-level domain',
            'numbers_in_domain': 'Numbers in domain name',
            'suspicious_keywords': 'Suspicious keywords present',
            'excessive_subdomains': 'Excessive subdomains',
            'long_url': 'Unusually long URL',
            'ip_in_url': 'IP address in URL',
            'shortened_url': 'URL shortening service used'
        };
        
        for (const [key, value] of Object.entries(features)) {
            const li = document.createElement('li');
            
            // Format feature name
            const featureName = featureDescriptions[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            // Set icon and class based on feature value
            let icon, featureClass;
            
            if (value) {
                // For phishing features, true is bad
                icon = 'fa-circle-exclamation';
                featureClass = 'feature-danger';
                li.innerHTML = `<i class="fas ${icon} ${featureClass}"></i> ${featureName}: <span class="${featureClass}">Detected</span>`;
            } else {
                // For phishing features, false is good
                icon = 'fa-circle-check';
                featureClass = 'feature-safe';
                li.innerHTML = `<i class="fas ${icon} ${featureClass}"></i> ${featureName}: <span class="${featureClass}">Not Detected</span>`;
            }
            
            featureList.appendChild(li);
        }
        
        // Show result card
        resultCard.style.display = 'block';
    }
    
    // Function to display error
    function displayError(url, error) {
        // Update analyzed URL
        analyzedUrl.textContent = url;
        
        // Update result header
        resultCard.className = 'result-card warning';
        resultIcon.className = 'fas fa-exclamation-circle';
        resultTitle.textContent = 'Analysis Error';
        
        // Update verdict
        verdict.textContent = 'Unable to Analyze';
        confidence.textContent = 'An error occurred during analysis';
        
        // Clear and update feature list
        featureList.innerHTML = '';
        const li = document.createElement('li');
        li.innerHTML = `<i class="fas fa-times feature-danger"></i> Error: ${error.message}`;
        featureList.appendChild(li);
        
        // Show result card
        resultCard.style.display = 'block';
    }
});