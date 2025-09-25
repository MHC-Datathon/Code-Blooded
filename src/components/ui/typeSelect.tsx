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
      <SelectTrigger className="w-[160px]">
        <SelectValue placeholder="Select a month" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="MOBILE DOUBLE PARKED">Double parking</SelectItem>
        <SelectItem value="MOBILE BUS LANE">Bus lane</SelectItem>
        <SelectItem value="MOBILE BUS STOP">Bus stop</SelectItem>
        {/* ...etc */}
      </SelectContent>
    </Select>
  )
}