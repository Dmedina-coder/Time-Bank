import React, { useCallback, useContext, useEffect, useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { AuthContext } from '../context/AuthContext';
import * as api from '../services/api';
import './BuyCredits.css';

// ── Formulario interno de pago (necesita estar dentro de <Elements>) ──
const CheckoutForm = ({ credits, clientSecret, onSuccess, onCancel }) => {
  const stripe = useStripe();
  const elements = useElements();

  const [paying, setPaying] = useState(false);
  const [payError, setPayError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!stripe || !elements) return;

    try {
      setPaying(true);
      setPayError(null);

      const { error, paymentIntent } = await stripe.confirmPayment({
        elements,
        confirmParams: { return_url: window.location.href },
        redirect: 'if_required'
      });

      if (error) {
        setPayError(error.message);
        return;
      }

      if (paymentIntent && paymentIntent.status === 'succeeded') {
        await onSuccess(paymentIntent.id);
      } else {
        setPayError('El pago no se completó. Inténtalo de nuevo.');
      }
    } catch (err) {
      setPayError(err.message);
    } finally {
      setPaying(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="checkout-form">
      <div className="checkout-summary">
        Comprando <strong>{credits} crédito{credits !== 1 ? 's' : ''}</strong>
      </div>

      <PaymentElement />

      {payError && <div className="alert alert-error">{payError}</div>}

      <div className="checkout-actions">
        <button type="button" className="btn-outline" onClick={onCancel} disabled={paying}>
          Cancelar
        </button>
        <button type="submit" className="btn-primary" disabled={paying || !stripe}>
          {paying ? 'Procesando...' : 'Pagar'}
        </button>
      </div>
    </form>
  );
};

// ── Página principal ──
const BuyCredits = () => {
  const { refreshUser } = useContext(AuthContext);

  const [config, setConfig] = useState(null);
  const [configError, setConfigError] = useState(null);
  const [stripePromise, setStripePromise] = useState(null);

  const [credits, setCredits] = useState(5);
  const [step, setStep] = useState('choose'); // 'choose' | 'pay' | 'success'

  const [clientSecret, setClientSecret] = useState(null);
  const [intentError, setIntentError] = useState(null);
  const [creatingIntent, setCreatingIntent] = useState(false);

  const [successData, setSuccessData] = useState(null);

  useEffect(() => {
    api.getStripeConfig()
      .then(cfg => {
        setConfig(cfg);
        setStripePromise(loadStripe(cfg.public_key));
      })
      .catch(err => setConfigError(err.message));
  }, []);

  const handleContinue = async () => {
    if (credits < 1) return;
    try {
      setCreatingIntent(true);
      setIntentError(null);
      const data = await api.createStripePaymentIntent({ credits, currency: config?.currency });
      setClientSecret(data.client_secret);
      setStep('pay');
    } catch (err) {
      setIntentError(err.message);
    } finally {
      setCreatingIntent(false);
    }
  };

  const handleSuccess = useCallback(async (paymentIntentId) => {
    try {
      const data = await api.confirmStripePayment(paymentIntentId);
      setSuccessData(data);
      if (refreshUser) await refreshUser();
      setStep('success');
    } catch (err) {
      // Confirmación fallida: volver al paso previo con error
      setStep('choose');
      setIntentError(err.message);
    }
  }, [refreshUser]);

  const handleCancel = () => {
    setClientSecret(null);
    setStep('choose');
  };

  const pricePerCredit = config ? (config.credit_price_cents / 100).toFixed(2) : '—';
  const totalPrice = config ? ((credits * config.credit_price_cents) / 100).toFixed(2) : '—';
  const currency = (config?.currency || 'eur').toUpperCase();

  if (configError) {
    return (
      <div className="buy-credits-page">
        <div className="buy-credits-card">
          <h1>Comprar créditos</h1>
          <div className="alert alert-error">
            El sistema de pagos no está disponible en este momento: {configError}
          </div>
        </div>
      </div>
    );
  }

  if (!config) {
    return <div className="loading-state">Cargando opciones de pago...</div>;
  }

  return (
    <div className="buy-credits-page">
      <div className="buy-credits-card">
        <h1>Comprar créditos</h1>
        <p className="buy-credits-subtitle">
          Precio: <strong>{pricePerCredit} {currency}</strong> por crédito
        </p>

        {step === 'choose' && (
          <div className="choose-step">
            <div className="form-group">
              <label>Cantidad de créditos</label>
              <input
                type="number"
                min="1"
                max="500"
                value={credits}
                onChange={e => setCredits(Math.max(1, parseInt(e.target.value) || 1))}
              />
            </div>

            <div className="price-preview">
              Total a pagar: <strong>{totalPrice} {currency}</strong>
            </div>

            {intentError && <div className="alert alert-error">{intentError}</div>}

            <button
              className="btn-primary btn-full"
              onClick={handleContinue}
              disabled={creatingIntent || credits < 1}
            >
              {creatingIntent ? 'Preparando pago...' : `Pagar ${totalPrice} ${currency}`}
            </button>
          </div>
        )}

        {step === 'pay' && clientSecret && stripePromise && (
          <Elements stripe={stripePromise} options={{ clientSecret }}>
            <CheckoutForm
              credits={credits}
              clientSecret={clientSecret}
              onSuccess={handleSuccess}
              onCancel={handleCancel}
            />
          </Elements>
        )}

        {step === 'success' && successData && (
          <div className="success-step">
            <div className="success-icon">✅</div>
            <h2>¡Pago completado!</h2>
            <p>
              Se han añadido <strong>{successData.transaction?.credits} créditos</strong> a tu cuenta.
            </p>
            <p className="new-balance">
              Tu nuevo saldo: <strong>{successData.balance} créditos</strong>
            </p>
            <button className="btn-primary" onClick={() => { setStep('choose'); setSuccessData(null); }}>
              Comprar más créditos
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default BuyCredits;
