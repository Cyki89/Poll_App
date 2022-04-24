import AdminSearchGroup from "./AdminSearchGroup";
import AdminActionGroup from "./AdminActionGroup";
import AdminSubtitleGroup from "./AdminSubtitleGroup";
import AdminAddItemGroup from "./AdminAddItemGroup";

const AdminPanelToolbar = ({
  subTitle,
  itemName,
  onAction,
  search,
  onSearch,
}) => {
  return (
    <div className="admin-panel-toolbar">
      <AdminSubtitleGroup subTitle={subTitle} />
      <AdminSearchGroup search={search} onSearch={onSearch} />
      <AdminActionGroup onAction={onAction} />
      <AdminAddItemGroup itemName={itemName} />
    </div>
  );
};

export default AdminPanelToolbar;
