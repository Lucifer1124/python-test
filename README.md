pipeline {
    agent any
    
    environment {
        // Centralized scanner configurations or tokens
        SONAR_TOKEN = credentials('sonar-auth-token')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com'
            }
        }

        // Step 2: Ensure no credentials are accidentally committed
        stage('Secret Scanning') {
            steps {
                echo 'Checking for hardcoded secrets...'
                // Example using TruffleHog or GitLeaks via Docker
                sh 'docker run --rm -v $(pwd):/pwd trufflesecurity/trufflehog:latest github --repo="file:///pwd"'
            }
        }

        // Step 3: Analyze code quality and vulnerabilities (SAST)
        stage('Static Application Security Testing (SAST)') {
            steps {
                echo 'Running SAST scan...'
                // Example using SonarQube CLI Scanner
                withSonarQubeEnv('SonarQubeServer') {
                    sh 'sonar-scanner -Dsonar.projectKey=static-app -Dsonar.sources=.'
                }
            }
        }

        // Step 4: Check open-source dependencies for known flaws (SCA)
        stage('Software Composition Analysis (SCA)') {
            steps {
                echo 'Checking node_modules or dependencies for vulnerabilities...'
                // Example using npm audit for JS apps or OWASP Dependency-Check
                sh 'npm audit --audit-level=high'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying secure static application to hosting environment...'
                // Deployment steps go here
            }
        }
    }
    
    post {
        always {
            cleanWs() // Always clean workspace to maintain runner hygiene
        }
    }
}
SECURITY GROOVY CODE EXAMPLE 
ARCHITECTURE

  [ Jenkins Agent ] (Runs inside Private VPC)
               │
      ┌────────┴────────┬───────────────────┐
      ▼                 ▼                   ▼
[ GitLeaks ]      [ Semgrep OSS ]     [ OWASP Dependency-Check ]
(Local Scan)       (Local Rules)       (Local Database Mirror)
      │                 │                   │
      └────────┬────────┴───────────────────┘
               ▼
   [ DefectDojo Vulnerability Portal ] (Self-Hosted On-Premise)
