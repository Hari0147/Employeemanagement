pipeline {
    agent any
    
    stages {
        stage('fetchCode') {
            steps {
                git branch: 'main', credentialsId: 'gitcred', url: 'https://github.com/Hari0147/Employeemanagement.git'
            }
        }
        stage('Build') {
            steps {
                sh '/var/lib/jenkins/.local/bin/pyb clean publish'
            }
        }
        stage('DockerImage') {
            steps {
                sh 'docker build -t hari00147/python-application .'
            }
        }
        stage('pushImageToDocker') {
            steps {
                withCredentials([string(credentialsId: 'Docker', variable: 'Docker')]) {
                  sh '''
                  echo "$Docker" | docker login -u hari00147 --password-stdin
                  docker push hari00147/python-application:latest
                  '''
                }
            }
        }
        stage('DeployToContainerInK8s') {
            steps {
                sh 'kubectl apply -f k8s.yml'
            }
        }
    }
}
