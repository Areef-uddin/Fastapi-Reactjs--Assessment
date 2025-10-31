import React, {useEffect, useState} from 'react'

export default function TaskForm({onSaved, editing, onCancel, apiBase}){
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  useEffect(()=>{
    if(editing){
      setTitle(editing.title || '')
      setDescription(editing.description || '')
    } else {
      setTitle('')
      setDescription('')
    }
  }, [editing])

  async function submit(e){
    e.preventDefault()
    const payload = { title, description }
    if(editing){
      await fetch(`${apiBase}/tasks/${editing.id}`, {
        method:"PUT", headers:{"Content-Type":"application/json"}, body: JSON.stringify(payload)
      })
      onSaved()
      onCancel()
    } else {
      await fetch(`${apiBase}/tasks/`, {
        method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(payload)
      })
      onSaved()
      setTitle(''); setDescription('')
    }
  }

  return (
    <form onSubmit={submit} style={{marginBottom:20}}>
      <input placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} required style={{padding:8,width:'100%'}}/>
      <textarea placeholder="Description" value={description} onChange={e=>setDescription(e.target.value)} style={{padding:8,width:'100%',marginTop:8}}/>
      <div style={{marginTop:8}}>
        <button type="submit" style={{padding:'8px 12px'}}>{editing ? 'Update' : 'Create'}</button>
        {editing && <button type="button" onClick={onCancel} style={{marginLeft:8}}>Cancel</button>}
      </div>
    </form>
  )
}
