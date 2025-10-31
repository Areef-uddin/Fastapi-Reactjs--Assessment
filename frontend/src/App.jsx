import React, {useEffect, useState} from 'react'
import TaskForm from './TaskForm'
import TaskList from './TaskList'

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000"

export default function App(){
  const [tasks, setTasks] = useState([])
  const [editing, setEditing] = useState(null)

  async function fetchTasks(){
    const r = await fetch(`${API_BASE}/tasks/`)
    const data = await r.json()
    setTasks(data)
  }

  useEffect(()=>{ fetchTasks() }, [])

  return (
    <div style={{padding:20, fontFamily:'sans-serif', maxWidth:800, margin:'0 auto'}}>
      <h1>Tasks (No DB)</h1>
      <TaskForm onSaved={fetchTasks} editing={editing} onCancel={()=>setEditing(null)} apiBase={API_BASE} />
      <TaskList tasks={tasks} onEdit={t=>setEditing(t)} onDeleted={fetchTasks} apiBase={API_BASE} onRefresh={fetchTasks} />
    </div>
  )
}
