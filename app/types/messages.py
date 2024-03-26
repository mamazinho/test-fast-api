from pydantic import BaseModel, Field


class GetObjectIdView(BaseModel):
    id: str = Field(alias="_id")


class ConversationMessage(BaseModel):
    text: str


class Location(BaseModel):
    degreesLatitude: float
    degreesLongitude: float


class LocationMessage(BaseModel):
    location: Location


class Row(BaseModel):
    title: str
    rowId: str
    description: str | None = None


class Section(BaseModel):
    title: str
    rows: list[Row]


class ListMessage(BaseModel):
    text: str
    footer: str
    title: str
    buttonText: str
    sections: list[Section]


class UrlButton(BaseModel):
    displayText: str
    url: str


class QuickReplyButton(BaseModel):
    id: str
    displayText: str


class CallButton(BaseModel):
    displayText: str
    phoneNumber: str


class TemplateButton(BaseModel):
    index: int
    urlButton: UrlButton | None = None
    callButton: CallButton | None = None
    quickReplyButton: QuickReplyButton | None = None


class TemplateMessage(BaseModel):
    text: str
    footer: str
    templateButtons: list[TemplateButton]


class ButtonText(BaseModel):
    displayText: str


class Button(BaseModel):
    buttonId: str
    buttonText: ButtonText
    type: int = 1


class ButtonMessage(BaseModel):
    text: str
    footer: str
    buttons: list[Button]
    headerType: int = 1


class Audio(BaseModel):
    url: str


class AudioMessage(BaseModel):
    audio: Audio
    ptt: bool = True
    mimetype: str | None = None

    text_before: str | None = None
    text_after: str | None = None


class Video(BaseModel):
    url: str


class VideoMessage(BaseModel):
    video: Video
    caption: str | None = None
    gifPlayback: bool = False


class Document(BaseModel):
    url: str


class DocumentMessage(BaseModel):
    document: Document


class Image(BaseModel):
    url: str


class ImageMessage(BaseModel):
    image: Image
    caption: str | None = None


class SendToMessage(BaseModel):
    message_uuid: str
    sequence_name: str
    message_name: str


class Action(BaseModel):
    add_tags: list[str] | None = None
    remove_tags: list[str] | None = None
    send_to_message: SendToMessage | None = None


class AttendanceAssigned(BaseModel):
    attendant_id: str
    attendant_name: str


class TriggerActivated(BaseModel):
    trigger_id: str
    trigger_type: str
    trigger_answer: str
    actions: list[Action] | None = None


class CapturedText(BaseModel):
    match_text: str
    pattern_text: str
    actions: list[Action] | None = None


class NotificationEvent(BaseModel):
    attendance_assigned: AttendanceAssigned | None = None
    trigger_activated: TriggerActivated | None = None
    captured_text: CapturedText | None = None


class Message(BaseModel):
    conversation: ConversationMessage | None = None
    location: LocationMessage | None = None
    list: ListMessage | None = None
    template: TemplateMessage | None = None
    button: ButtonMessage | None = None
    image: ImageMessage | None = None
    audio: AudioMessage | None = None
    video: VideoMessage | None = None
    document: DocumentMessage | None = None
    notification_event: NotificationEvent | None = None

    @property
    def content(self):
        return (
            self.conversation
            or self.location
            or self.list
            or self.template
            or self.button
            or self.image
            or self.audio
            or self.video
            or self.document
            or self.notification_event
        )

    @property
    def text(self):
        if self.conversation:
            return self.conversation.text
        elif self.audio:
            return self.audio.text_after or self.audio.text_before
        elif self.video:
            return self.video.caption
        elif self.image:
            return self.image.caption

    def set_text(self, text):
        if self.conversation:
            self.conversation.text = text
        elif self.audio:
            if self.audio.text_after:
                self.audio.text_after = text
            elif self.audio.text_before:
                self.audio.text_before = text
        elif self.video:
            self.video.caption = text
        elif self.image:
            self.image.caption = text
