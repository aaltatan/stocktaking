import Alpine, { type Alpine as AlpineType } from "alpinejs";
import htmx from "htmx.org";
import "./style.css";

declare global {
  interface Window {
    Alpine: AlpineType;
    htmx: typeof htmx;
  }
}

// htmx configurations
document.addEventListener("htmx:load", () => {
  htmx.config.defaultSwapStyle = "outerHTML";
  htmx.config.globalViewTransitions = true;
  htmx.config.refreshOnHistoryMiss = true;
  htmx.config.historyCacheSize = 0;
  htmx.config.historyRestoreAsHxRequest = false;
});

Alpine.start();
