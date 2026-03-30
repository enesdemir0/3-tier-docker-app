import React, { useState } from 'react';
import { Send, Bot, User, BookOpen, Loader2 } from 'lucide-react';
import { sendMessage } from './services/api';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // 📡 Calling your FastAPI Backend!
      const data = await sendMessage(input);
      
      const aiMessage = { 
        role: 'bot', 
        content: data.generation,
        sources: data.documents 
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { role: 'bot', content: "Oops! My brain is tired. Please check the backend connection." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-900 text-slate-100 font-sans">
      {/* Header */}
      <header className="p-4 bg-slate-800 border-b border-slate-700 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="p-2 bg-blue-600 rounded-lg">
            <Bot size={24} className="text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">AI Knowledge Assistant</h1>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-6 max-w-4xl mx-auto w-full">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex gap-3 max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`p-2 rounded-full h-10 w-10 flex items-center justify-center ${msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-700'}`}>
                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              <div className={`p-4 rounded-2xl ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-800 border border-slate-700'}`}>
                <p className="leading-relaxed">{msg.content}</p>
                
                {/* 📚 Sources/Documents Section */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-slate-700">
                    <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">
                      <BookOpen size={14} /> Sources
                    </div>
                    <div className="grid grid-cols-1 gap-2">
                      {msg.sources.map((src, i) => (
                        <div key={i} className="text-xs bg-slate-900/50 p-2 rounded italic text-slate-400">
                          "{src.substring(0, 150)}..."
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-center gap-3 bg-slate-800 p-4 rounded-2xl border border-slate-700">
              <Loader2 className="animate-spin text-blue-500" size={20} />
              <span className="text-slate-400 italic">Thinking...</span>
            </div>
          </div>
        )}
      </main>

      {/* Input Area */}
      <footer className="p-6 bg-slate-900">
        <div className="max-w-4xl mx-auto relative">
          <input
            className="w-full bg-slate-800 border border-slate-700 rounded-2xl p-4 pr-16 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-100"
            placeholder="Ask your documents something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button 
            onClick={handleSend}
            disabled={isLoading}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-blue-600 hover:bg-blue-500 rounded-xl transition-colors disabled:opacity-50"
          >
            <Send size={20} className="text-white" />
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;