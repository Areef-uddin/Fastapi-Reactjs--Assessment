import React from 'react'

export default function TaskList({tasks, onEdit, onDeleted, apiBase, onRefresh}){
  async function deleteTask(id){
    if(!confirm('Delete this task?')) return
    await fetch(`${apiBase}/tasks/${id}`, {method:'DELETE'})
    onDeleted()
  }

  return (
    <div>
      {tasks.length === 0 && <div>No tasks yet</div>}
      {tasks.map(t => (
        <div key={t.id} style={{border:'1px solid #ddd', padding:12, marginBottom:8}}>
          <h3>{t.title}</h3>
          <p>{t.description}</p>
          <button onClick={()=>onEdit(t)}>Edit</button>
          <button onClick={()=>deleteTask(t.id)} style={{marginLeft:8}}>Delete</button>
        </div>
      ))}
    </div>
  )
}
