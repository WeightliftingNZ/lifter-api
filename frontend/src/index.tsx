/** @format */

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";
import "./index.css";
import App from "./App";
import ReactGA from "react-ga4";

const queryClient = new QueryClient();

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

root.render(
  <QueryClientProvider client={queryClient}>
    <Router>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </Router>
    <ReactQueryDevtools initialIsOpen={false} />
  </QueryClientProvider>
);

const googleAnalyticsGId = process.env.REACT_APP_G_ID ?? "Nill";
ReactGA.initialize(googleAnalyticsGId);
ReactGA.send("pageview");
