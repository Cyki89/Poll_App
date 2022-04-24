const createKey = (column, idx) => `${idx}${column.label}`;

const TableHeaders = ({ columns, sortOrder, sortColumn, onSort }) => {
  const renderSortIcon = (column) => {
    if (!column.sortable) return;

    let sortIconClass = "sortoptions clickable";
    if (!sortColumn || column.path !== sortColumn)
      return <i className={sortIconClass}></i>;

    sortIconClass =
      sortOrder === "asc"
        ? "sortoptions sort-ascending clickable"
        : "sortoptions sort-descending clickable";

    return <i className={sortIconClass}></i>;
  };

  return (
    <thead>
      <tr>
        {columns.map((column, idx) => (
          <th
            key={createKey(column, idx)}
            onClick={column.sortable ? (e) => onSort(column.path) : null}>
            {column.label} {renderSortIcon(column)}
          </th>
        ))}
      </tr>
    </thead>
  );
};

export default TableHeaders;
