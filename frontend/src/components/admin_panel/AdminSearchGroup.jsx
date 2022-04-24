import FormControl from "react-bootstrap/FormControl";
import searchIcon from "./../../search.svg";
import Button from "react-bootstrap/Button";
import { useState } from "react";

const AdminSearchGroup = ({ search, onSearch }) => {
  const [searchValue, setSearchValue] = useState(() => search);

  const handleSearch = () => {
    if (searchValue === "") return;
    onSearch(searchValue);
  };

  return (
    <div className="admin-panel-toolbar-item">
      <img src={searchIcon} className="search-icon" alt="" />
      <FormControl
        className="admin-panel-input"
        placeholder="Questionnaire..."
        value={searchValue}
        onChange={(e) => {
          setSearchValue(e.target.value);
        }}
      />
      <Button className="admin-panel-btn" onClick={handleSearch}>
        Search
      </Button>
    </div>
  );
};

export default AdminSearchGroup;
