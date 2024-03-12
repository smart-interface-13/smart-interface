import neptune.new as neptune

# Inicializa tu proyecto en Neptune (necesitas tu API token)
# Puedes obtener tu API token registrándote en https://neptune.ai/
run = neptune.init(project='mariakimm/SMART-INTERFACE', api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI3MTFjYjhmZi05YTIzLTQ0NGMtYmE5Yy0yYTNmODk1MjgyYjYifQ==')

# Registra los parámetros de tu experimento
params = {
    'learning_rate': 0.001,
    'batch_size': 32,
    'epochs': 10
}
run['parameters'] = params

# Código para cargar y preparar tus datos, entrenar y evaluar tu modelo...
train_data, test_data, validation_data = prepare_data()

# Ejemplo: Entrenamiento del modelo
for epoch in range(epochs):
    # Código para un paso de entrenamiento...
    train_loss, train_accuracy = train_step(train_data)
    
    # Registra las métricas en Neptune
    run['train/loss'].log(train_loss)
    run['train/accuracy'].log(train_accuracy)
    
    # Código para un paso de validación...
    validation_loss, validation_accuracy = evaluate_model(validation_data)
    
    # Registra las métricas de validación en Neptune
    run['validation/loss'].log(validation_loss)
    run['validation/accuracy'].log(validation_accuracy)

# Cierra el experimento en Neptune
run.stop()