let started = false;

function preserveMaxInitData() {
  const bridgeData = window.WebApp?.initData?.trim();
  if (bridgeData) {
    window.KVS_MAX_INIT_DATA = bridgeData;
    return;
  }

  // MAX also supplies WebAppData in the URL fragment. Save it before the
  // single-page router replaces that fragment with a route such as #/events.
  // The backend still validates this signed value; this only prevents a race
  // between the bridge loading and the app starting.
  const fragment = window.location.hash.replace(/^#/, '');
  const fragmentData = new URLSearchParams(fragment).get('WebAppData')?.trim();
  if (fragmentData) window.KVS_MAX_INIT_DATA = fragmentData;
}

function startApplication() {
  if (started) return;
  started = true;
  preserveMaxInitData();
  import('./main.js').catch((error) => {
    console.error('Failed to start KVS Job miniapp', error);
    const app = document.querySelector('#app');
    if (app) {
      app.innerHTML = `
        <main class="screen">
          <section class="state-card">
            <strong>Не удалось запустить приложение</strong>
            <p>Обновите страницу. Если ошибка повторится, сообщите администратору.</p>
          </section>
        </main>`;
    }
  });
}

const hostname = window.location.hostname;
const isLocal = hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1';

// MAX Bridge is unnecessary in a regular local browser. Skipping the remote
// script keeps development usable without internet access or access to st.max.ru.
if (isLocal || window.WebApp) {
  startApplication();
} else {
  const bridge = document.createElement('script');
  bridge.src = 'https://st.max.ru/js/max-web-app.js';
  bridge.async = true;
  bridge.addEventListener('load', () => {
    preserveMaxInitData();
    startApplication();
  }, { once: true });
  bridge.addEventListener('error', startApplication, { once: true });
  document.head.append(bridge);

  // A temporary MAX CDN failure must never leave the user on a blank screen.
  window.setTimeout(startApplication, 3000);
}
