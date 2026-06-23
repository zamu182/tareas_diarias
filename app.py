@app.route('/api/tareas')
def api_tareas():
    # Obtenemos TODAS las tareas para que se visualicen en el calendario
    todas = Tarea.query.all()
    
    eventos = []
    for t in todas:
        # Lógica de colores según el estado de la tarea
        if t.completo:
            color = '#28a745'  # Verde: Tarea finalizada con éxito
        elif t.archivada:
            color = '#6c757d'  # Gris: Tarea solo archivada
        else:
            # Colores según prioridad para tareas activas (pendientes)
            if t.prioridad == 'Alta':
                color = '#dc3545'
            elif t.prioridad == 'Media':
                color = '#ffc107'
            else:
                color = '#198754'
            
        eventos.append({
            'title': t.texto,
            'start': t.fecha,
            'color': color
        })
        
    return jsonify(eventos)