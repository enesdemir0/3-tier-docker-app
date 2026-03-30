import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, BookOpen, Loader2, Link as LinkIcon } from 'lucide-react';
import { sendMessage } from './services/api';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when a new message arrives
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendMessage(input);
      
      const aiMessage = { 
        role: 'bot', 
        content: data.generation,
        sources: data.sources // Array of {url, content}
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { 
        role: 'bot', 
        content: "I encountered a connection error. Please make sure the backend is running on port 8000." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#0f172a] text-slate-100 font-sans">
      {/* 🚀 Header */}
      <header className="p-4 bg-[#1e293b] border-b border-slate-700/50 shadow-xl z-10">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600 rounded-xl shadow-lg shadow-blue-500/20">
              <Bot size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">Agentic RAG Assistant</h1>
              <p className="text-[10px] text-blue-400 font-mono uppercase tracking-widest">Enterprise Intelligence Tier</p>
            </div>
          </div>
        </div>
      </header>

      {/* 💬 Chat Window */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-8 max-w-5xl mx-auto w-full scrollbar-thin scrollbar-thumb-slate-700">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-40">
            <Bot size={64} className="text-slate-500" />
            <p className="text-xl font-medium">How can I help you today?</p>
            <p className="text-sm max-w-xs">Ask questions about AI Agents, RAG, or search the web in real-time.</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex gap-4 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`flex-shrink-0 p-2.5 rounded-xl h-10 w-10 flex items-center justify-center shadow-lg ${msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-800 border border-slate-700'}`}>
                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              
              <div className={`p-5 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-[#1e293b] border border-slate-700/50'}`}>
                <p className="leading-relaxed whitespace-pre-wrap text-sm md:text-base">{msg.content}</p>
                
                {/* 📚 SOURCES SECTION */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-6 pt-5 border-t border-slate-700/50">
                    <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 mb-3 uppercase tracking-[0.2em]">
                      <BookOpen size={14} /> Referenced Sources
                    </div>
                    <div className="grid grid-cols-1 gap-3">
                      {msg.sources.map((src, i) => (
                        <div key={i} className="group bg-slate-900/50 p-4 rounded-xl border border-slate-700/30 hover:border-blue-500/30 transition-all">
                          <a 
                            href={src.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="flex items-center gap-2 text-blue-400 hover:text-blue-300 font-semibold text-xs mb-2 transition-colors overflow-hidden"
                          >
                            <LinkIcon size={12} className="flex-shrink-0" />
                            <span className="truncate underline decoration-blue-500/20">Source {i+1}: {src.url}</span>
                          </a>
                          <p className="text-[11px] text-slate-400 leading-relaxed italic">
                            "{src.content.length > 250 ? src.content.substring(0, 250) + '...' : src.content}"
                          </p>
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
            <div className="flex items-center gap-4 bg-[#1e293b] p-5 rounded-2xl border border-slate-700/50">
              <Loader2 className="animate-spin text-blue-500" size={24} />
              <span className="text-slate-400 font-medium animate-pulse">Analyzing knowledge bases...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* ⌨️ Input Section */}
      <footer className="p-6 bg-[#0f172a] border-t border-slate-800/50">
        <div className="max-w-5xl mx-auto relative group">
          <input
            className="w-full bg-[#1e293b] border border-slate-700/50 rounded-2xl p-5 pr-16 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-slate-100 placeholder:text-slate-500 shadow-2xl"
            placeholder="Type your message here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button 
            onClick={handleSend}
            disabled={isLoading}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl transition-all disabled:opacity-30 disabled:cursor-not-allowed shadow-lg shadow-blue-500/20"
          >
            <Send size={20} />
          </button>
        </div>
        <p className="text-center text-[10px] text-slate-600 mt-4">Enterprise Agentic RAG System v1.0 • Connected to Groq & Pinecone</p>
      </footer>
    </div>
  );
}

export default App;