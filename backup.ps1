# Load Configurations
$POSTGRES_CONFIG = @{
  dbname   = "your_db"
  user     = "your_user"
  password = "your_password"
  host     = "your_host"
  port     = "5432"
}

$AZURE_STORAGE_CONFIG = @{
  accountName   = "your_account_name"
  accountKey    = "your_account_key"
  containerName = "your_container_name"
}

# Generate Dump File Name with Timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "backup_$timestamp.sql"

# PostgreSQL Dump Command
$env:PGPASSWORD = $POSTGRES_CONFIG.password
$dumpCommand = "pg_dump -h $($POSTGRES_CONFIG.host) -p $($POSTGRES_CONFIG.port) -U $($POSTGRES_CONFIG.user) -F c -b -v -f $backupFile $($POSTGRES_CONFIG.dbname)"

try {
  Write-Host "Starting database dump..."
  Invoke-Expression $dumpCommand
  Write-Host "Database dump successful: $backupFile"
} catch {
  Write-Host "Error dumping database: $_"
  exit 1
}

# Azure Blob Storage Connection
$storageContext = New-AzStorageContext -StorageAccountName $AZURE_STORAGE_CONFIG.accountName -StorageAccountKey $AZURE_STORAGE_CONFIG.accountKey

# Upload to Azure Blob Storage
try {
  Write-Host "Uploading $backupFile to Azure Blob Storage..."
  Set-AzStorageBlobContent -File $backupFile -Container $AZURE_STORAGE_CONFIG.containerName -Blob $backupFile -Context $storageContext -Force
  Write-Host "Backup uploaded successfully: $backupFile"
} catch {
  Write-Host "Error uploading to Azure Blob Storage: $_"
  exit 1
}

# Cleanup Local Backup File
try {
  Remove-Item -Path $backupFile -Force
  Write-Host "Local backup file deleted: $backupFile"
} catch {
  Write-Host "Error deleting local backup file: $_"
}