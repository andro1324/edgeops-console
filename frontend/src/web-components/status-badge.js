class StatusBadge extends HTMLElement {
  static observedAttributes = ['status'];

  connectedCallback() { this.render(); }
  attributeChangedCallback() { this.render(); }

  render() {
    const status = (this.getAttribute('status') || 'unknown').toLowerCase();
    const label = this.textContent?.trim() || status;
    this.innerHTML = `<span class="wc-status wc-status--${status}"><span class="wc-status__dot"></span>${label}</span>`;
  }
}

if (!customElements.get('status-badge')) customElements.define('status-badge', StatusBadge);