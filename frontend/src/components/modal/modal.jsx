import Modal from "react-modal";
import style from "./modal.module.css"

export default function MyModal({showModal, setShowModal, children, ...props}){

    // const renderBackdrop = (props) => <div className={style.backdrop} {...props} />;
    const handleClose = () => setShowModal(false);
    return(
        <Modal
            isOpen={showModal} // Отображаем модальное окно, если showModal = true
            onRequestClose={handleClose} // Закрытие модального окна при клике вне окна или на "Esc"
            className={props.className ? props.className : style.modal} // Стили модального окна
            overlayClassName={style.backdrop} // Стили для фонового слоя (backdrop)
            style={props.style} // Inline-стили, если переданы через props
        >
            {children}
        </Modal>
    )
}