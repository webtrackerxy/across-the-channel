import { useEffect, useRef, type ReactNode } from "react";
import { X } from "lucide-react";
export function Dialog({
  open,
  title,
  onClose,
  children,
}: {
  open: boolean;
  title: string;
  onClose: () => void;
  children: ReactNode;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    if (open && !ref.current?.open) ref.current?.showModal();
    else if (!open && ref.current?.open) ref.current.close();
  }, [open]);
  return (
    <dialog
      className="content-dialog"
      ref={ref}
      aria-label={title}
      onCancel={onClose}
      onClose={onClose}
    >
      <header className="dialog-header">
        <h2>{title}</h2>
        <button
          className="icon-button"
          onClick={onClose}
          aria-label={`Close ${title}`}
        >
          <X size={20} />
        </button>
      </header>
      <div className="dialog-content">{children}</div>
    </dialog>
  );
}
