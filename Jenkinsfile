pipeline {
    agent any

    stages{
        stage('Cloning from Github....'){
            steps{
                script{
                    echo 'Cloning from Github ....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/MananJain2464/Anime_recommedation_system.git']])
                }
            }
        }
    }
}