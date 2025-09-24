import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

type Props = {
  value: string | null
  onChange: (val: string) => void
}

export function TypeSelect({ value, onChange }: Props) {
  return (
    <Select value={value ?? ""} onValueChange={onChange}>
      <SelectTrigger className="w-[150px]">
        <SelectValue placeholder="Select a month" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="doubleParking">Double parking</SelectItem>
        <SelectItem value="busLane">Bus lane</SelectItem>
        <SelectItem value="busStop">Bus stop</SelectItem>
        <SelectItem value="total">Total</SelectItem>
        {/* ...etc */}
      </SelectContent>
    </Select>
  )
}