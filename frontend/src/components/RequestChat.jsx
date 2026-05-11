import React, { useContext, useEffect, useRef, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import * as api from '../services/api';
import './RequestChat.css';

const RequestChat = ({ request, onClose }) => {
  const { user } = useContext(AuthContext);

  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState(null);

  const bottomRef = useRef(null);

  const fetchMessages = async () => {
    try {
      setError(null);
      const data = await api.getRequestMessages(request.id, { per_page: 100 });
      setMessages(data.items || []);
      // Marcar como leídos los mensajes que no son míos y están sin leer
      for (const msg of data.items || []) {
        if (!msg.read_at && msg.sender_id !== user?.id) {
          api.markMessageAsRead(request.id, msg.id).catch(() => {});
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, [request.id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    const content = newMessage.trim();
    if (!content) return;
    try {
      setSending(true);
      setSendError(null);
      const msg = await api.sendRequestMessage(request.id, content);
      setMessages(prev => [...prev, msg]);
      setNewMessage('');
    } catch (err) {
      setSendError(err.message);
    } finally {
      setSending(false);
    }
  };

  const formatTime = (iso) => {
    if (!iso) return '';
    return new Date(iso).toLocaleString('es-ES', { dateStyle: 'short', timeStyle: 'short' });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="chat-modal" onClick={e => e.stopPropagation()}>
        <div className="chat-modal-header">
          <div>
            <h2>Mensajes</h2>
            <p className="chat-subtitle">
              {request.service_title || `Solicitud #${request.id}`} ·{' '}
              <span>{request.requester_name}</span> ↔ <span>{request.provider_name}</span>
            </p>
          </div>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <div className="chat-messages">
          {loading && <div className="chat-loading">Cargando mensajes...</div>}
          {error && <div className="chat-error">{error}</div>}
          {!loading && !error && messages.length === 0 && (
            <div className="chat-empty">No hay mensajes todavía. ¡Sé el primero en escribir!</div>
          )}
          {messages.map(msg => {
            const isMine = msg.sender_id === user?.id;
            return (
              <div key={msg.id} className={`chat-bubble ${isMine ? 'bubble-mine' : 'bubble-other'}`}>
                {!isMine && <span className="bubble-sender">{msg.sender_name}</span>}
                <div className="bubble-content">{msg.content}</div>
                <div className="bubble-meta">
                  <span className="bubble-time">{formatTime(msg.created_at)}</span>
                  {isMine && (
                    <span className="bubble-read">
                      {msg.read_at ? '✓✓' : '✓'}
                    </span>
                  )}
                </div>
              </div>
            );
          })}
          <div ref={bottomRef} />
        </div>

        <form className="chat-input-area" onSubmit={handleSend}>
          {sendError && <div className="chat-send-error">{sendError}</div>}
          <div className="chat-input-row">
            <input
              type="text"
              value={newMessage}
              onChange={e => setNewMessage(e.target.value)}
              placeholder="Escribe un mensaje..."
              disabled={sending}
              maxLength={1000}
              autoFocus
            />
            <button type="submit" disabled={sending || !newMessage.trim()}>
              {sending ? '...' : 'Enviar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RequestChat;
