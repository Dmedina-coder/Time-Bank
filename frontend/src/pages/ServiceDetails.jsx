import React, { useContext, useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import * as api from '../services/api';
import ReviewComponent, { StarRating } from '../components/ReviewComponent';
import './ServiceDetails.css';

const ServiceDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal solicitar
  const [showRequestModal, setShowRequestModal] = useState(false);
  const [scheduledDate, setScheduledDate] = useState('');
  const [requestError, setRequestError] = useState(null);
  const [requesting, setRequesting] = useState(false);
  const [requestSuccess, setRequestSuccess] = useState(false);

  // Subida de imagen
  const [uploadingImage, setUploadingImage] = useState(false);
  const [imageError, setImageError] = useState(null);
  const [imageSuccess, setImageSuccess] = useState(false);
  const imageInputRef = React.useRef(null);

  // Reviews
  const [reviews, setReviews] = useState([]);
  const [avgRating, setAvgRating] = useState(null);
  const [reviewForm, setReviewForm] = useState({ rating: 5, comment: '' });
  const [reviewError, setReviewError] = useState(null);
  const [reviewSuccess, setReviewSuccess] = useState(false);
  const [submittingReview, setSubmittingReview] = useState(false);
  const [canReview, setCanReview] = useState(false);

  const handleImageUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setUploadingImage(true);
      setImageError(null);
      setImageSuccess(false);
      const updated = await api.uploadServiceImage(id, file);
      setService(prev => ({ ...prev, has_image: updated.has_image }));
      setImageSuccess(true);
    } catch (err) {
      setImageError(err.message);
    } finally {
      setUploadingImage(false);
      e.target.value = '';
    }
  };

  useEffect(() => {
    const fetchService = async () => {
      try {
        setLoading(true);
        const data = await api.getService(id);
        setService(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchService();
  }, [id]);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const data = await api.getServiceReviews(id);
        setReviews(data.items ?? []);
        setAvgRating(data.avg_rating ?? null);
      } catch {
        // silencioso
      }
    };
    fetchReviews();
  }, [id, reviewSuccess]);

  useEffect(() => {
    if (!user || !service) return;
    if (user.id === service.owner_id) return;
    const checkCanReview = async () => {
      try {
        const requests = await api.getRequests({ status: 'completed', service_id: id });
        const items = requests.items ?? [];
        const userCompleted = items.some(r => r.requester_id === user.id);
        const alreadyReviewed = reviews.some(r => r.reviewer_id === user.id);
        setCanReview(userCompleted && !alreadyReviewed);
      } catch {
        setCanReview(false);
      }
    };
    checkCanReview();
  }, [user, service, id, reviews]);

  const handleRequestSubmit = async (e) => {
    e.preventDefault();
    if (!scheduledDate) {
      setRequestError('Selecciona una fecha para el servicio.');
      return;
    }
    try {
      setRequesting(true);
      setRequestError(null);
      await api.createRequest({
        service_id: parseInt(id),
        scheduled_date: new Date(scheduledDate).toISOString()
      });
      setRequestSuccess(true);
      setShowRequestModal(false);
    } catch (err) {
      setRequestError(err.message);
    } finally {
      setRequesting(false);
    }
  };

  const isOwner = user && service && user.id === service.owner_id;
  const canRequest = user && service && !isOwner && service.status === 'active';

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    setReviewError(null);
    try {
      setSubmittingReview(true);
      await api.createReview({
        service_id: parseInt(id),
        rating: reviewForm.rating,
        comment: reviewForm.comment
      });
      setReviewSuccess(true);
      setReviewForm({ rating: 5, comment: '' });
      setCanReview(false);
    } catch (err) {
      setReviewError(err.message);
    } finally {
      setSubmittingReview(false);
    }
  };

  if (loading) return <div className="loading-state">Cargando servicio...</div>;
  if (error) return (
    <div className="service-details-page">
      <div className="alert alert-error">{error}</div>
      <Link to="/services" className="btn-outline">← Volver a servicios</Link>
    </div>
  );
  if (!service) return null;

  return (
    <div className="service-details-page">
      <div className="breadcrumb">
        <Link to="/services">Servicios</Link> / <span>{service.title}</span>
      </div>

      <div className="service-details-card">
        {service.has_image && (
          <div className="service-details-image">
            <img
              src={api.getServiceImageUrl(id)}
              alt={service.title}
              onError={e => { e.target.closest('.service-details-image').style.display = 'none'; }}
            />
          </div>
        )}
        <div className="service-details-header">
          <div>
            <span className="service-category-badge">{service.category}</span>
            <h1>{service.title}</h1>
            <p className="service-owner-info">
              Ofrecido por <strong>{service.owner?.name || service.owner_name}</strong>
            </p>
          </div>
          <div className={`status-pill status-${service.status}`}>
            {service.status === 'active' ? 'Disponible' : 'No disponible'}
          </div>
        </div>

        <div className="service-details-body">
          <h3>Descripción</h3>
          <p className="service-full-description">{service.description}</p>
          <div className="service-credits-info">
            <span className="credits-label">Coste del servicio:</span>
            <span className="credits-value">⏱ {service.credits ?? 1} crédito{(service.credits ?? 1) !== 1 ? 's' : ''}</span>
          </div>
        </div>

        <div className="service-details-footer">
          <p className="service-date">
            Publicado el {service.created_at ? new Date(service.created_at).toLocaleDateString('es-ES') : '—'}
          </p>
          <div className="service-actions">
            {requestSuccess && (
              <div className="alert alert-success">
                ¡Solicitud enviada correctamente! Ve a <Link to="/requests">Mis solicitudes</Link> para hacer seguimiento.
              </div>
            )}
            {canRequest && !requestSuccess && (
              <button className="btn-primary" onClick={() => { setShowRequestModal(true); setRequestError(null); }}>
                Solicitar este servicio
              </button>
            )}
            {isOwner && (
              <>
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp,image/gif"
                  ref={imageInputRef}
                  style={{ display: 'none' }}
                  onChange={handleImageUpload}
                />
                <button
                  className="btn-outline"
                  onClick={() => { setImageError(null); setImageSuccess(false); imageInputRef.current?.click(); }}
                  disabled={uploadingImage}
                >
                  {uploadingImage ? 'Subiendo...' : (service.has_image ? '🖼 Cambiar imagen' : '🖼 Subir imagen')}
                </button>
                {imageError && <span className="alert alert-error" style={{ fontSize: '0.85rem', padding: '0.3rem 0.7rem' }}>{imageError}</span>}
                {imageSuccess && <span className="alert alert-success" style={{ fontSize: '0.85rem', padding: '0.3rem 0.7rem' }}>¡Imagen actualizada!</span>}
                <Link to="/services" className="btn-outline">Gestionar mis servicios</Link>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Sección de valoraciones */}
      <div className="reviews-section">
        <div className="reviews-section-header">
          <h2>Valoraciones</h2>
          {avgRating !== null && (
            <div className="avg-rating">
              <StarRating rating={Math.round(avgRating)} />
              <span className="avg-rating-value">{avgRating} / 5</span>
              <span className="avg-rating-count">({reviews.length} {reviews.length === 1 ? 'valoración' : 'valoraciones'})</span>
            </div>
          )}
        </div>

        {canReview && !reviewSuccess && (
          <form className="review-form" onSubmit={handleReviewSubmit}>
            <h3>Deja tu valoración</h3>
            {reviewError && <div className="alert alert-error">{reviewError}</div>}
            <div className="form-group">
              <label>Puntuación</label>
              <div className="star-selector">
                {[1, 2, 3, 4, 5].map(n => (
                  <button
                    type="button"
                    key={n}
                    className={`star-btn ${n <= reviewForm.rating ? 'filled' : ''}`}
                    onClick={() => setReviewForm(f => ({ ...f, rating: n }))}
                    aria-label={`${n} estrellas`}
                  >★</button>
                ))}
              </div>
            </div>
            <div className="form-group">
              <label>Comentario (opcional)</label>
              <textarea
                value={reviewForm.comment}
                onChange={e => setReviewForm(f => ({ ...f, comment: e.target.value }))}
                placeholder="Describe tu experiencia con este servicio..."
                rows={3}
                maxLength={1000}
              />
            </div>
            <button type="submit" className="btn-primary" disabled={submittingReview}>
              {submittingReview ? 'Enviando...' : 'Publicar valoración'}
            </button>
          </form>
        )}

        {reviewSuccess && (
          <div className="alert alert-success">¡Gracias por tu valoración!</div>
        )}

        {reviews.length === 0 ? (
          <p className="no-reviews">Aún no hay valoraciones para este servicio.</p>
        ) : (
          <div className="reviews-list">
            {reviews.map(r => <ReviewComponent key={r.id} review={r} />)}
          </div>
        )}
      </div>

      {/* Modal solicitar */}
      {showRequestModal && (
        <div className="modal-overlay" onClick={() => setShowRequestModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Solicitar servicio</h2>
              <button className="modal-close" onClick={() => setShowRequestModal(false)}>✕</button>
            </div>
            <form onSubmit={handleRequestSubmit} className="modal-form">
              <p className="modal-service-name">
                Estás solicitando: <strong>{service.title}</strong>
              </p>
              <p className="modal-credits-notice">
                Se descontarán <strong>{service.credits ?? 1} crédito{(service.credits ?? 1) !== 1 ? 's' : ''}</strong> de tu saldo al completarse el servicio.
              </p>
              {requestError && <div className="alert alert-error">{requestError}</div>}
              <div className="form-group">
                <label>Fecha y hora deseada</label>
                <input
                  type="datetime-local"
                  value={scheduledDate}
                  onChange={e => setScheduledDate(e.target.value)}
                  min={new Date().toISOString().slice(0, 16)}
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-outline" onClick={() => setShowRequestModal(false)}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary" disabled={requesting}>
                  {requesting ? 'Enviando...' : 'Enviar solicitud'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ServiceDetails;
