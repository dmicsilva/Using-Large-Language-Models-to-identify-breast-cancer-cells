import json
import plotly.graph_objs as go

# Load the JSON data
with open('preparationDocument/repsona-20250715010238.json') as f:
    data = json.load(f)

# Extract the tasks with their start and end dates
tasks = []
for task in data['tasks'][1]:
    tasks.append({
        'task': task['name'],
        'start_date': task['startDate'] // 1000,  # Convert to seconds
        'end_date': task['dueDate'] // 1000  # Convert to seconds
    })

# Create the Gantt chart
fig = go.Figure(data=[
    go.Bar(
        name=task['task'],
        x=[(task['start_date'] + (task['end_date'] - task['start_date'])) / 2],  # Calculate midpoint of date range
        width=(task['end_date'] - task['start_date']) / (60 * 60 * 24),  # Convert to days
        y=[1],
        marker_color='blue'
    ) for task in tasks
])

# Update the layout
fig.update_layout(
    title='Gantt Chart',
    xaxis_title='Date',
    yaxis_title='',
    bargroupgap=0,
    barmode='stack',
    showlegend=False
)

# Save the Gantt chart as a PNG file
png_filename = 'gantt_chart.png'
fig.write_image(png_filename)