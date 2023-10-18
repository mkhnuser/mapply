import { QueryClient, QueryClientProvider } from "react-query";

import Header from "./ui/Header";
import Content from "./features/content/Content";
import Footer from "./ui/Footer";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="h-screen flex flex-col place-content-between">
        <Header />
        <Content />
      </div>
      {/* Display the footer only if a user scrolls down. */}
      <Footer />
    </QueryClientProvider>
  );
}

export default App;
