import React from 'react';
import CreatePage from './CreatePage';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-50 to-purple-50">
      <header className="p-6 bg-white shadow-lg flex justify-center">
        <h1 className="text-3xl font-bold text-blue-700">AI App Builder</h1>
      </header>
      <main className="p-8">
        <CreatePage />
      </main>
    </div>
  );
}

export default App;
