import Header from "./ui/Header";
import Content from "./ui/Content";
import Footer from "./ui/Footer";
import { LatLngLiteral } from "leaflet";

const positions: LatLngLiteral[] = [
  { lat: 55, lng: 39 },
  { lat: 58, lng: 38 },
  { lat: 45, lng: 38 },
  { lat: 61, lng: 44 },
  { lat: 80, lng: 80 },
];

function App() {
  return (
    <>
      <div className="h-screen flex flex-col place-content-between">
        <Header />
        <Content positions={positions} />
      </div>
      {/* Display the footer only if user scrolls down. */}
      <Footer />
    </>
  );
}

export default App;
