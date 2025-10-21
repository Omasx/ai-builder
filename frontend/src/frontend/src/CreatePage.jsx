import React, { useState, useEffect } from 'react';

function CreatePage() {
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [status, setStatus] = useState(null);
  const [projectId, setProjectId] = useState(null);

  async function submit() {
    setStatus({phase: "queued"});
    const res = await fetch("/api/create", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({title, description: desc})
    });
    const j = await res.json();
    setStatus(j.detail || {phase: "queued"});
    setProjectId(j.project_id);
    pollStatus(j.project_id);
  }

  async function pollStatus(pid){
    const interval = 3000;
    const poll = async ()=>{
      try{
        const r = await fetch(`/api/status/${pid}`);
        const j = await r.json();
        setStatus(j);
        if(j.phase && (j.phase === "ready" || j.phase === "error" || j.phase === "failed")){
          return;
        }
      }catch(e){}
      setTimeout(poll, interval);
    };
    poll();
  }

  return (
    <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg">
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Create Your AI App</h2>
      <input
        value={title}
        onChange={(e)=>setTitle(e.target.value)}
        placeholder="Project Title"
        className="w-full p-3 mb-4 border rounded"
      />
      <textarea
        value={desc}
        onChange={(e)=>setDesc(e.target.value)}
        placeholder="Describe your app"
        className="w-full p-3 mb-4 border rounded"
      />
      <button onClick={submit} className="w-full py-3 bg-blue-600 text-white font-semibold rounded">
        Create App
      </button>

      <div className="mt-6 p-4 bg-gray-100 rounded text-gray-800">
        <pre>{JSON.stringify(status, null, 2)}</pre>
        {status && status.phase === "ready" && projectId && (
          <a className="inline-block mt-3 px-4 py-2 bg-green-600 text-white rounded" href={`/projects/${projectId}/`} target="_blank" rel="noreferrer">
            Open Preview
          </a>
        )}
      </div>
    </div>
  );
}

export default CreatePage;
